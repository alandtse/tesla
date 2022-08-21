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

        if self._car.is_climate_on:
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
        return self._car.inside_temp

    @property
    def max_temp(self):
        """Return the max temperature."""
        if self._car.max_avail_temp:
            return self._car.max_avail_temp

        return DEFAULT_MAX_TEMP

    @property
    def min_temp(self):
        """Return the min temperature"""
        if self._car.min_avail_temp:
            return self._car.min_avail_temp

        return DEFAULT_MIN_TEMP

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._car.driver_temp_setting

    async def async_set_temperature(self, **kwargs):
        """Set new target temperatures."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature:
            _LOGGER.debug("%s: Setting temperature to %s", self.name, temperature)

            temp = round(temperature, 1)

            await self._car.set_temperature(temp)
            # We'll create a non-blocking update call so we don't hold up
            # the current call.
            await self.update_controller(
                force=True, wake_if_asleep=True, blocking=False
            )

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        _LOGGER.debug("%s: Setting hvac mode to %s", self.name, hvac_mode)
        if hvac_mode == HVAC_MODE_OFF:
            await self._car.set_hvac_mode("off")
        elif hvac_mode == HVAC_MODE_HEAT_COOL:
            await self._car.set_hvac_mode("on")

        # Changing the HVAC mode can change alot of climate parms
        # So we'll do a blocking update.
        await self.update_controller(force=True, wake_if_asleep=True)

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode, e.g., home, away, temp.

        Requires SUPPORT_PRESET_MODE.
        """
        if self._car.defrost_mode == 2:
            return "Defrost"

        if self._car.climate_keeper_mode == "dog":
            return "Dog Mode"

        if self._car.climate_keeper_mode == "camp":
            return "Camp Mode"

        if self._car.climate_keeper_mode == "on":
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

            if self._car.defrost_mode != 0:
                await self._car.set_max_defrost(False)

            if self._car.climate_keeper_mode != 0:
                await self._car.set_climate_keeper_mode(0)

        elif preset_mode == "Defrost":
            await self._car.set_max_defrost(True)

        else:
            await self._car.set_climate_keeper_mode(KEEPER_MAP[preset_mode])

        # Changing the Climate modes mode can change alot of climate parms
        # So we'll do a blocking update.
        await self.update_controller(force=True, wake_if_asleep=True)
