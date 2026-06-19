"""Support for Tesla locks."""

import logging

from homeassistant.components.lock import LockEntity, LockEntityFeature
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
        entities.append(TeslaCarDoors(car, coordinator))
        entities.append(TeslaCarChargePortLatch(car, coordinator))

    async_add_entities(entities, update_before_add=True)


class TeslaCarDoors(TeslaCarEntity, LockEntity):
    """Representation of a Tesla car door lock."""

    type = "doors"

    def _ensure_vehicle_state(self) -> None:
        """Ensure vehicle_state can be updated after lock commands."""
        if not isinstance(self._car._vehicle_data.get("vehicle_state"), dict):
            self._car._vehicle_data["vehicle_state"] = {}

    async def async_lock(self, **kwargs):
        """Send lock command."""
        _LOGGER.debug("Locking: %s", self.name)
        self._ensure_vehicle_state()
        await self._car.lock()
        self.async_write_ha_state()

    async def async_unlock(self, **kwargs):
        """Send unlock command."""
        _LOGGER.debug("Unlocking: %s", self.name)
        self._ensure_vehicle_state()
        await self._car.unlock()
        self.async_write_ha_state()

    @property
    def is_locked(self):
        """Return True if door is locked."""
        vehicle_state = self._car._vehicle_data.get("vehicle_state")
        if not isinstance(vehicle_state, dict):
            return None
        return self._car.is_locked


class TeslaCarChargePortLatch(TeslaCarEntity, LockEntity):
    """Representation of a Tesla charge port latch."""

    type = "charge port latch"
    _attr_icon = "mdi:ev-plug-tesla"
    _attr_supported_features = LockEntityFeature.OPEN

    async def async_open(self, **kwargs):
        """Send open command."""
        _LOGGER.debug("Opening: %s", self.name)
        await self._car.charge_port_door_open()
        self.async_write_ha_state()

    async def async_unlock(self, **kwargs):
        """Send unlock command."""
        _LOGGER.debug("Unlocking: %s", self.name)
        await self._car.charge_port_door_open()
        self.async_write_ha_state()

    async def async_lock(self, **kwargs):
        """Log lock command not possible."""
        _LOGGER.debug("Locking charge port latch not possible with Tesla's API.")

    @property
    def is_locked(self) -> bool:
        """Return True if charge port latch is engaged."""
        return self._car.charge_port_latch == "Engaged"
