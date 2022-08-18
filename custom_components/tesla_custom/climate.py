"""Support for Tesla HVAC system."""
from __future__ import annotations

import logging

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    DEFAULT_MAX_TEMP,
    DEFAULT_MIN_TEMP,
    HVAC_MODE_HEAT_COOL,
    HVAC_MODE_OFF,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS, TEMP_FAHRENHEIT
from homeassistant.core import HomeAssistant
from teslajsonpy.exceptions import UnknownPresetMode

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SUPPORT_HVAC = [HVAC_MODE_HEAT_COOL, HVAC_MODE_OFF]
SUPPORT_PRESET = ["Normal", "Defrost", "Keep On", "Dog Mode", "Camp Mode"]

KEEPER_MAP = {
    "Keep On": 1,
    "Dog Mode": 2,
    "Camp Mode": 3,
}


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla CLimate by config_entry."""
    entities = [
        TeslaClimate(
            hass,
            car,
            hass.data[DOMAIN][config_entry.entry_id]["coordinator"],
        )
        for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]
    ]
    async_add_entities(entities, True)


class TeslaClimate(TeslaCarDevice, ClimateEntity):
    """Representation of a Tesla climate."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "HVAC (climate) system"

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

    @property
    def hvac_mode(self):
        """Return hvac operation ie. heat, cool mode.

        Need to be one of HVAC_MODE_*.
        """

        if self.car.climate.get("is_climate_on", False):
            return HVAC_MODE_HEAT_COOL

        return HVAC_MODE_OFF

    @property
    def hvac_modes(self):
        """Return the list of available hvac operation modes.

        Need to be a subset of HVAC_MODES.
        """
        return SUPPORT_HVAC

    @property
    def temperature_unit(self):
        """Return the unit of measurement.

        Tesla API always returns in Celsius.
        """
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self.car.climate.get("inside_temp")

    @property
    def max_temp(self):
        """Return the max temperature."""
        return self.car.climate.get("max_avail_temp", DEFAULT_MAX_TEMP)

    @property
    def min_temp(self):
        """Return the min temperature"""
        return self.car.climate.get("min_avail_temp", DEFAULT_MIN_TEMP)

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self.car.climate.get("driver_temp_setting")

    async def async_set_temperature(self, **kwargs):
        """Set new target temperatures."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature:
            _LOGGER.debug("%s: Setting temperature to %s", self.name, temperature)

            temp = round(temperature, 1)

            data = await self._send_command(
                "CHANGE_CLIMATE_TEMPERATURE_SETTING",
                path_vars={"vehicle_id": self.car.id},
                driver_temp=temp,
                passenger_temp=temp,
                wake_if_asleep=True,
            )

            if data and data["response"]["result"]:
                self.car.climate["driver_temp_setting"] = temp
                self.async_write_ha_state()

            # We'll create a non-blocking update call so we don't hold up
            # the current call.
            await self.update_controller(
                force=True, wake_if_asleep=True, blocking=False
            )

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        _LOGGER.debug("%s: Setting hvac mode to %s", self.name, hvac_mode)
        if hvac_mode == HVAC_MODE_OFF:
            await self._send_command(
                "CLIMATE_OFF",
                path_vars={"vehicle_id": self.car.id},
                wake_if_asleep=True,
            )
        elif hvac_mode == HVAC_MODE_HEAT_COOL:
            await self._send_command(
                "CLIMATE_ON",
                path_vars={"vehicle_id": self.car.id},
                wake_if_asleep=True,
            )

        # Changing the HVAC mode can change alot of climate parms
        # So we'll do a blocking update.
        await self.update_controller(force=True, wake_if_asleep=True)

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode, e.g., home, away, temp.

        Requires SUPPORT_PRESET_MODE.
        """
        if self.car.climate.get("defrost_mode", 0) == 2:
            return "Defrost"

        keeper_mode = self.car.climate.get("climate_keeper_mode", "")
        if keeper_mode == "dog":
            return "Dog Mode"

        if keeper_mode == "camp":
            return "Camp Mode"

        if keeper_mode == "on":
            return "Keep On"

        return "Normal"

    @property
    def preset_modes(self) -> list[str] | None:
        """Return a list of available preset modes.

        Requires SUPPORT_PRESET_MODE.
        """
        return SUPPORT_PRESET

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        _LOGGER.debug("%s: Setting preset_mode to: %s", self.name, preset_mode)

        if preset_mode == "Normal":
            # If setting Normal, we need to check Defrost And Keep modes.

            if self.car.climate.get("defrost_mode") != 0:
                await self._send_command(
                    "MAX_DEFROST",
                    path_vars={"vehicle_id": self.car.id},
                    on=False,
                    wake_if_asleep=True,
                )

            if self.car.climate.get("climate_keeper_mode") != 0:
                await self._send_command(
                    "SET_CLIMATE_KEEPER_MODE",
                    path_vars={"vehicle_id": self.car.id},
                    climate_keeper_mode=0,
                    wake_if_asleep=True,
                )

        elif preset_mode == "Defrost":
            await self._send_command(
                "MAX_DEFROST",
                path_vars={"vehicle_id": self.car.id},
                on=True,
                wake_if_asleep=True,
            )

        else:
            keeper_id = KEEPER_MAP[preset_mode]
            await self._send_command(
                "SET_CLIMATE_KEEPER_MODE",
                path_vars={"vehicle_id": self.car.id},
                climate_keeper_mode=keeper_id,
                wake_if_asleep=True,
            )

        # Changing the Climate modes mode can change alot of climate parms
        # So we'll do a blocking update.
        await self.update_controller(force=True, wake_if_asleep=True)
