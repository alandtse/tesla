"""Support for Tesla locks."""
import logging

from homeassistant.components.lock import LockEntity, LockEntityFeature
from homeassistant.core import HomeAssistant
from teslajsonpy.car import TeslaCar

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla locks by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    entities = []

    for car in cars.values():
        entities.append(TeslaCarDoors(hass, car, coordinator))
        entities.append(TeslaCarChargePortLatch(hass, car, coordinator))

    async_add_entities(entities, True)


class TeslaCarDoors(TeslaCarEntity, LockEntity):
    """Representation of a Tesla car door lock."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize door lock entity."""
        super().__init__(hass, car, coordinator)
        self.type = "doors"

    async def async_lock(self, **kwargs):
        """Send lock command."""
        _LOGGER.debug("Locking: %s", self.name)
        await self._car.lock()
        await self.async_update_ha_state()

    async def async_unlock(self, **kwargs):
        """Send unlock command."""
        _LOGGER.debug("Unlocking: %s", self.name)
        await self._car.unlock()
        await self.async_update_ha_state()

    @property
    def is_locked(self):
        """Return True if door is locked."""
        return self._car.is_locked


class TeslaCarChargePortLatch(TeslaCarEntity, LockEntity):
    """Representation of a Tesla charge port latch."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize charge port latch (lock) entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charge port latch"
        self._attr_icon = "mdi:ev-plug-tesla"
        self._attr_supported_features = LockEntityFeature.OPEN

    async def async_open(self, **kwargs):
        """Send open command."""
        _LOGGER.debug("Opening: %s", self.name)
        await self._car.charge_port_door_open()
        await self.async_update_ha_state()

    async def async_unlock(self, **kwargs):
        """Send unlock command."""
        _LOGGER.debug("Unlocking: %s", self.name)
        await self._car.charge_port_door_open()
        await self.async_update_ha_state()

    async def async_lock(self, **kwargs):
        """Log lock command not possible."""
        _LOGGER.debug("Locking charge port latch not possible with Tesla's API.")

    @property
    def is_locked(self):
        """Return True if charge port latch is engaged."""
        if self._car.charge_port_latch == "Engaged":
            return True
        return False
