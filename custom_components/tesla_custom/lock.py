"""Support for Tesla door locks."""
import logging

from teslajsonpy.car import TeslaCar

from homeassistant.components.lock import LockEntity
from homeassistant.core import HomeAssistant

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    entities = []

    for car in cars.values():
        entities.append(Trunk(hass, car, coordinator))
        entities.append(Frunk(hass, car, coordinator))
        entities.append(Doors(hass, car, coordinator))
        entities.append(ChargerDoor(hass, car, coordinator))

    async_add_entities(entities, True)


class Trunk(TeslaCarDevice, LockEntity):
    """Representation of a Tesla door lock."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Lock Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "trunk lock"

    async def async_lock(self, **kwargs):
        """Send the lock command."""
        _LOGGER.debug("Locking doors for: %s", self.name)
        if self.is_locked is False:
            await self._car.toggle_trunk()

    async def async_unlock(self, **kwargs):
        """Send the unlock command."""
        _LOGGER.debug("Unlocking doors for: %s", self.name)
        if self.is_locked is True:
            await self._car.toggle_trunk()

    @property
    def is_locked(self):
        """Get whether the trunk is in locked state."""
        return self._car.is_trunk_locked


class Frunk(TeslaCarDevice, LockEntity):
    """Representation of a Tesla docar: TeslaCaraCar"""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Lock Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "frunk lock"

    async def async_lock(self, **kwargs):
        """Send the lock command."""
        _LOGGER.debug("Locking doors for: %s", self.name)
        if self.is_locked is False:
            await self._car.toggle_frunk()

    async def async_unlock(self, **kwargs):
        """Send the unlock command."""
        _LOGGER.debug("Unlocking doors for: %s", self.name)
        if self.is_locked is True:
            await self._car.toggle_frunk()

    @property
    def is_locked(self):
        """Get whether the lock is in locked state."""
        return self._car.is_frunk_locked


class Doors(TeslaCarDevice, LockEntity):
    """Representation of a Tesla door lock."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Lock Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "door lock"

    async def async_lock(self, **kwargs):
        """Send the lock command."""
        _LOGGER.debug("Locking doors for: %s", self.name)
        await self._car.lock()

    async def async_unlock(self, **kwargs):
        """Send the unlock command."""
        _LOGGER.debug("Unlocking doors for: %s", self.name)
        await self._car.unlock()

    @property
    def is_locked(self):
        """Get whether the lock is in locked state."""
        return self._car.is_locked


class ChargerDoor(TeslaCarDevice, LockEntity):
    """Representation of a Tesla Charger door lock."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Lock Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charger door lock"

    async def async_lock(self, **kwargs):
        """Send the lock command."""
        _LOGGER.debug("Locking doors for: %s", self.name)
        await self._car.charge_port_door_close()

    async def async_unlock(self, **kwargs):
        """Send the unlock command."""
        _LOGGER.debug("Unlocking doors for: %s", self.name)
        await self._car.charge_port_door_open()

    @property
    def is_locked(self):
        """Get whether the lock is in locked state."""
        charge_door_open = self._car.charge_port_door_open
        charger_latched = self._car.charge_port_latch == "Engaged"

        if charger_latched:
            return True

        return charge_door_open is False
