"""Support for Tesla locks."""
import logging

from teslajsonpy.car import TeslaCar

from homeassistant.components.lock import LockEntity
from homeassistant.core import HomeAssistant

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
        entities.append(TeslaCarTrunk(hass, car, coordinator))
        entities.append(TeslaCarFrunk(hass, car, coordinator))
        entities.append(TeslaCarDoors(hass, car, coordinator))
        entities.append(TeslaCarChargerDoor(hass, car, coordinator))

    async_add_entities(entities, True)


class TeslaCarTrunk(TeslaCarEntity, LockEntity):
    """Representation of a Tesla car trunk lock."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize trunk lock entity."""
        super().__init__(hass, car, coordinator)
        self.type = "trunk lock"

    async def async_lock(self, **kwargs):
        """Send lock command."""
        _LOGGER.debug("Locking: %s", self.name)
        if self.is_locked is False:
            await self._car.toggle_trunk()
            await self.async_update_ha_state()

    async def async_unlock(self, **kwargs):
        """Send unlock command."""
        _LOGGER.debug("Unlocking: %s", self.name)
        if self.is_locked is True:
            await self._car.toggle_trunk()
            await self.async_update_ha_state()

    @property
    def is_locked(self):
        """Return True is trunk is locked."""
        return self._car.is_trunk_locked


class TeslaCarFrunk(TeslaCarEntity, LockEntity):
    """Representation of a Tesla car frunk lock."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize frunk lock entity."""
        super().__init__(hass, car, coordinator)
        self.type = "frunk lock"

    async def async_lock(self, **kwargs):
        """Send lock command."""
        _LOGGER.debug("Locking: %s", self.name)
        if self.is_locked is False:
            await self._car.toggle_frunk()
            await self.async_update_ha_state()

    async def async_unlock(self, **kwargs):
        """Send unlock command."""
        _LOGGER.debug("Unlocking: %s", self.name)
        if self.is_locked is True:
            await self._car.toggle_frunk()
            await self.async_update_ha_state()

    @property
    def is_locked(self):
        """Return True if frunk is locked."""
        return self._car.is_frunk_locked


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
        self.type = "door lock"

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


class TeslaCarChargerDoor(TeslaCarEntity, LockEntity):
    """Representation of a Tesla car charger door lock."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize charger door lock entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charger door lock"

    async def async_lock(self, **kwargs):
        """Send lock command."""
        _LOGGER.debug("Locking: %s", self.name)
        await self._car.charge_port_door_close()
        await self.async_update_ha_state()

    async def async_unlock(self, **kwargs):
        """Send unlock command."""
        _LOGGER.debug("Unlocking: %s", self.name)
        await self._car.charge_port_door_open()
        await self.async_update_ha_state()

    @property
    def is_locked(self):
        """Return True if charger door is latched."""
        charge_door_open = self._car.charge_port_door_open
        charger_latched = self._car.charge_port_latch == "Engaged"

        if charger_latched:
            return True

        return charge_door_open is False
