"""Support for Tesla HVAC system."""
from __future__ import annotations

import logging

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT_COOL,
    HVAC_MODE_OFF,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS, TEMP_FAHRENHEIT
from homeassistant.util import slugify

from teslajsonpy.exceptions import UnknownPresetMode

from . import DOMAIN as TESLA_DOMAIN
from .tesla_device import TeslaDevice
from .helpers import get_device, enable_entity

_LOGGER = logging.getLogger(__name__)

SUPPORT_HVAC = [HVAC_MODE_HEAT_COOL, HVAC_MODE_OFF]

CLIMATE_DEVICES = [
    ["switch", "heated steering switch", "steering_wheel_heater"],
    ["select", "heated seat left", "seat_heater_left"],
    ["select", "heated seat right", "seat_heater_right"],
    ["select", "heated seat rear_left", "seat_heater_rear_left"],
    ["select", "heated seat rear_center", "seat_heater_rear_center"],
    ["select", "heated seat rear_right", "seat_heater_rear_right"],
    ["select", "heated seat third_row_left", "seat_heater_third_row_left"],
    ["select", "heated seat third_row_right", "seat_heater_third_row_right"],
]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Tesla binary_sensors by config_entry."""
    async_add_entities(
        [
            TeslaThermostat(
                device,
                hass.data[TESLA_DOMAIN][config_entry.entry_id]["coordinator"],
            )
            for device in hass.data[TESLA_DOMAIN][config_entry.entry_id]["devices"][
                "climate"
            ]
        ],
        True,
    )


class TeslaThermostat(TeslaDevice, ClimateEntity):
    """Representation of a Tesla climate."""

    def __init__(self, tesla_device, coordinator):
        """Initialize of the sensor."""
        super().__init__(tesla_device, coordinator)
        self._entities_enabled = False

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

    @property
    def hvac_mode(self):
        """Return hvac operation ie. heat, cool mode.

        Need to be one of HVAC_MODE_*.
        """
        if self.tesla_device.is_hvac_enabled():
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
        """Return the unit of measurement."""
        if self.tesla_device.measurement == "F":
            return TEMP_FAHRENHEIT
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self.tesla_device.get_current_temp()

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self.tesla_device.get_goal_temp()

    @TeslaDevice.Decorators.check_for_reauth
    async def async_set_temperature(self, **kwargs):
        """Set new target temperatures."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature:
            _LOGGER.debug("%s: Setting temperature to %s", self.name, temperature)
            await self.tesla_device.set_temperature(temperature)
            self.async_write_ha_state()

    @TeslaDevice.Decorators.check_for_reauth
    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        _LOGGER.debug("%s: Setting hvac mode to %s", self.name, hvac_mode)
        if hvac_mode == HVAC_MODE_OFF:
            await self.tesla_device.set_status(False)
        elif hvac_mode == HVAC_MODE_HEAT_COOL:
            await self.tesla_device.set_status(True)
        await self.update_climate_related_devices()
        self.async_write_ha_state()

    @TeslaDevice.Decorators.check_for_reauth
    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        _LOGGER.debug("%s: Setting preset_mode to: %s", self.name, preset_mode)
        try:
            await self.tesla_device.set_preset_mode(preset_mode)
            self.async_write_ha_state()
        except UnknownPresetMode as ex:
            _LOGGER.error("%s", ex.message)

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode, e.g., home, away, temp.

        Requires SUPPORT_PRESET_MODE.
        """
        return self.tesla_device.preset_mode

    @property
    def preset_modes(self) -> list[str] | None:
        """Return a list of available preset modes.

        Requires SUPPORT_PRESET_MODE.
        """
        return self.tesla_device.preset_modes

    def refresh(self) -> None:
        """Refresh data."""

        super().refresh()

        if self._entities_enabled:
            # Already enabled all required entities before.
            return

        vin = self.tesla_device.vin()

        # Get all the climate parameters so we can determine what is supported by this vin.
        # pylint: disable=protected-access
        climate_params = self.tesla_device._controller.get_climate_params(vin=vin)
        if climate_params is None or len(climate_params) == 0:
            # No data available
            _LOGGER.debug("No data available for vin %s", vin)
            return

        # Loop through the climate devices
        for c_device in CLIMATE_DEVICES:
            if climate_params.get(c_device[2], None) is None:
                # This climate device is not available.
                _LOGGER.debug(
                    "Device %s (%s) not available for vin %s",
                    c_device[1],
                    c_device[2],
                    vin,
                )
                continue

            # Determine unique id for this entity.
            unique_id = slugify(
                f"Tesla Model {str(vin[3]).upper()} {vin[-6:]} {c_device[1]}"
            )
            enable_entity(self.hass, c_device[0], TESLA_DOMAIN, unique_id)
        self._entities_enabled = True

    async def update_climate_related_devices(self):
        """Reset the Manual Update time on climate related devices.

        This way, their states are correctly reflected if they are dependant on the Climate state.
        """

        # This is really gross, and i kinda hate it.
        # but its the only way i could figure out how to force an update on the underlying device
        # thats in the teslajsonpy library.
        # This could be fixed by doing a pr in the underlying library,
        # but is ok for now.

        # This works by reseting the last update time in the underlying device.
        # this does not cause an api call, but instead enabled the undering device
        # to read from the shared climate data cache in the teslajsonpy library.

        # First, we need to force the controller to update, as the refresh functions asume it
        # has been uddated.
        # We have to manually update the controller becuase changing the HVAC state only updates its state in Home assistant,
        # and not the underlying cache in cliamte_parms. This does mean we talk to Tesla, but we only do so Once.

        # pylint: disable=protected-access
        await self.tesla_device._controller.update(
            self.tesla_device._id, wake_if_asleep=False, force=True
        )

        vin = self.tesla_device.vin()

        for c_device in CLIMATE_DEVICES:
            _LOGGER.debug("Refreshing Device: %s.%s", c_device[0], c_device[1])

            device = await get_device(
                self.hass, self.config_entry_id, c_device[0], c_device[1], vin
            )
            if device is not None:
                class_name = device.__class__.__name__
                attr_str = f"_{class_name}__manual_update_time"
                setattr(device, attr_str, 0)

                # Does not cause an API call.
                device.refresh()
