"""Support for Tesla covers."""

import logging

from homeassistant.components.cover import (
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.core import HomeAssistant

from .base import TeslaCarEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla locks by config_entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinators = entry_data["coordinators"]
    cars = entry_data["cars"]
    entities = []

    for vin, car in cars.items():
        coordinator = coordinators[vin]
        entities.append(TeslaCarChargerDoor(car, coordinator))
        entities.append(TeslaCarFrunk(car, coordinator))
        entities.append(TeslaCarTrunk(car, coordinator))
        entities.append(TeslaCarWindows(car, coordinator))

    async_add_entities(entities, update_before_add=True)


class TeslaCarChargerDoor(TeslaCarEntity, CoverEntity):
    """Representation of a Tesla car charger door cover."""

    type = "charger door"
    _attr_device_class = CoverDeviceClass.DOOR
    _attr_icon = "mdi:ev-plug-tesla"
    _attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

    async def async_close_cover(self, **kwargs):
        """Send close cover command."""
        _LOGGER.debug("Closing cover: %s", self.name)
        await self._car.charge_port_door_close()
        self.async_write_ha_state()

    async def async_open_cover(self, **kwargs):
        """Send open cover command."""
        _LOGGER.debug("Opening cover: %s", self.name)
        await self._car.charge_port_door_open()
        self.async_write_ha_state()

    @property
    def is_closed(self):
        """Return True if charger door is closed."""
        return not self._car.is_charge_port_door_open


class TeslaCarFrunk(TeslaCarEntity, CoverEntity):
    """Representation of a Tesla car frunk lock."""

    type = "frunk"
    _attr_device_class = CoverDeviceClass.DOOR
    _attr_icon = "mdi:car"

    async def async_close_cover(self, **kwargs):
        """Send close cover command."""
        _LOGGER.debug("Closing cover: %s", self.name)
        if self.is_closed is False:
            await self._car.toggle_frunk()
            self.async_write_ha_state()

    async def async_open_cover(self, **kwargs):
        """Send open cover command."""
        _LOGGER.debug("Opening cover: %s", self.name)
        if self.is_closed is True:
            await self._car.toggle_frunk()
            self.async_write_ha_state()

    @property
    def is_closed(self):
        """Return True if frunk is closed."""
        return self._car.is_frunk_closed

    @property
    def supported_features(self) -> int:
        """Return supported features."""
        # This check is for the trunk, need to find one for frunk
        if self._car.powered_lift_gate:
            return CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

        return CoverEntityFeature.OPEN


class TeslaCarTrunk(TeslaCarEntity, CoverEntity):
    """Representation of a Tesla car trunk cover."""

    type = "trunk"
    _attr_device_class = CoverDeviceClass.DOOR
    _attr_icon = "mdi:car-back"

    async def async_close_cover(self, **kwargs):
        """Send close cover command."""
        _LOGGER.debug("Closing cover: %s", self.name)
        if self.is_closed is False:
            await self._car.toggle_trunk()
            self.async_write_ha_state()

    async def async_open_cover(self, **kwargs):
        """Send open cover command."""
        _LOGGER.debug("Opening cover: %s", self.name)
        if self.is_closed is True:
            await self._car.toggle_trunk()
            self.async_write_ha_state()

    @property
    def is_closed(self):
        """Return True if trunk is closed."""
        return self._car.is_trunk_closed

    @property
    def supported_features(self) -> int:
        """Return supported features."""
        if self._car.powered_lift_gate:
            return CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

        return CoverEntityFeature.OPEN


class TeslaCarWindows(TeslaCarEntity, CoverEntity):
    """Representation of a Tesla car window cover."""

    type = "windows"
    _attr_device_class = CoverDeviceClass.AWNING
    _attr_icon = "mdi:car-door"
    _attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

    async def async_close_cover(self, **kwargs):
        """Send close cover command."""
        _LOGGER.debug("Closing cover: %s", self.name)
        if self.is_closed is False:
            await self._car.close_windows()
            self.async_write_ha_state()

    async def async_open_cover(self, **kwargs):
        """Send open cover command."""
        _LOGGER.debug("Opening cover: %s", self.name)
        if self.is_closed is True:
            await self._car.vent_windows()
            self.async_write_ha_state()

    @property
    def is_closed(self):
        """Return True if all windows are closed."""
        return self._car.is_window_closed
