"""Support for Tesla climate."""
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
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from teslajsonpy.car import TeslaCar

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SUPPORT_HVAC = [HVAC_MODE_HEAT_COOL, HVAC_MODE_OFF]
SUPPORT_PRESET = ["Normal", "Defrost", "Keep On", "Dog Mode", "Camp Mode"]

KEEPER_MAP = {
    "Keep On": 1,
    "Dog Mode": 2,
    "Camp Mode": 3,
}


async def async_setup_entry(
    hass: HomeAssistant, config_entry, async_add_entities
) -> None:
    """Set up the Tesla climate by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]

    entities = [
        TeslaCarClimate(
            hass,
            car,
            coordinator,
        )
        for car in cars.values()
    ]
    async_add_entities(entities, True)


class TeslaCarClimate(TeslaCarEntity, ClimateEntity):
    """Representation of a Tesla car climate."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize climate entity."""
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
        """Return list of available hvac operation modes.

        Need to be a subset of HVAC_MODES.
        """
        return SUPPORT_HVAC

    @property
    def temperature_unit(self):
        """Return unit of measurement.

        Tesla API always returns in Celsius.
        """
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return current temperature."""
        return self._car.inside_temp

    @property
    def max_temp(self):
        """Return max temperature."""
        if self._car.max_avail_temp:
            return self._car.max_avail_temp

        return DEFAULT_MAX_TEMP

    @property
    def min_temp(self):
        """Return min temperature."""
        if self._car.min_avail_temp:
            return self._car.min_avail_temp

        return DEFAULT_MIN_TEMP

    @property
    def target_temperature(self):
        """Return target temperature."""
        return self._car.driver_temp_setting

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature:
            _LOGGER.debug("%s: Setting temperature to %s", self.name, temperature)
            temp = round(temperature, 1)

            await self._car.set_temperature(temp)
            await self.async_update_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        _LOGGER.debug("%s: Setting hvac mode to %s", self.name, hvac_mode)
        if hvac_mode == HVAC_MODE_OFF:
            await self._car.set_hvac_mode("off")
        elif hvac_mode == HVAC_MODE_HEAT_COOL:
            await self._car.set_hvac_mode("on")
        # set_hvac_mode changes multiple states so refresh all entities
        await self._coordinator.async_refresh()

    @property
    def preset_mode(self):
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
    def preset_modes(self):
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
                await self._car.set_max_defrost(0)

            if self._car.climate_keeper_mode != 0:
                await self._car.set_climate_keeper_mode(0)

        elif preset_mode == "Defrost":
            await self._car.set_max_defrost(2)

        else:
            await self._car.set_climate_keeper_mode(KEEPER_MAP[preset_mode])
        # max_defrost changes multiple states so refresh all entities
        await self._coordinator.async_refresh()
