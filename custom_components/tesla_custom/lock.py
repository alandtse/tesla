"""Support for Tesla door locks."""
import logging

from homeassistant.components.lock import LockEntity
from homeassistant.core import HomeAssistant

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities = []
    for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]:
        entities.append(Trunk(hass, car, coordinator))
        entities.append(Frunk(hass, car, coordinator))
        entities.append(Doors(hass, car, coordinator))
        entities.append(ChargerDoor(hass, car, coordinator))

    async_add_entities(entities, True)


class Trunk(TeslaCarDevice, LockEntity):
    """Representation of a Tesla door lock."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Lock Entity."""
        super().__init__(hass, car, coordinator)
        self._name = "trunk lock"

    async def toggle_trunk(self):
        """Toggle Trunk lock."""
        data = await self._send_command(
            "ACTUATE_TRUNK",
            path_vars={"vehicle_id": self.car.id},
            which_trunk="rear",
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            return 1

    async def async_lock(self, **kwargs):
        """Send the lock command."""
        _LOGGER.debug("Locking doors for: %s", self.name)
        if self.is_locked is False:
            result = await self.toggle_trunk()
            if result == 1:
                self.car.state["rt"] = 0

        self.async_write_ha_state()

    async def async_unlock(self, **kwargs):
        """Send the unlock command."""
        _LOGGER.debug("Unlocking doors for: %s", self.name)
        if self.is_locked is True:
            result = await self.toggle_trunk()
            if result == 1:
                self.car.state["rt"] = 255

        self.async_write_ha_state()

    @property
    def is_locked(self):
        """Get whether the lock is in locked state."""
        return self.car.state.get("rt") == 0


class Frunk(TeslaCarDevice, LockEntity):
    """Representation of a Tesla door lock."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Lock Entity."""
        super().__init__(hass, car, coordinator)
        self._name = "frunk lock"

    async def toggle_trunk(self):
        """Toggle Frunk lock."""
        data = await self._send_command(
            "ACTUATE_TRUNK",
            path_vars={"vehicle_id": self.car.id},
            which_trunk="front",
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            return 1

    async def async_lock(self, **kwargs):
        """Send the lock command."""
        _LOGGER.debug("Locking doors for: %s", self.name)
        if self.is_locked is False:
            result = await self.toggle_trunk()
            if result == 1:
                self.car.state["ft"] = 0

        self.async_write_ha_state()

    async def async_unlock(self, **kwargs):
        """Send the unlock command."""
        _LOGGER.debug("Unlocking doors for: %s", self.name)
        if self.is_locked is True:
            result = await self.toggle_trunk()
            if result == 1:
                self.car.state["ft"] = 255

        self.async_write_ha_state()

    @property
    def is_locked(self):
        """Get whether the lock is in locked state."""
        return self.car.state.get("ft") == 0


class Doors(TeslaCarDevice, LockEntity):
    """Representation of a Tesla door lock."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Lock Entity."""
        super().__init__(hass, car, coordinator)
        self._name = "door lock"

    async def async_lock(self, **kwargs):
        """Send the lock command."""
        _LOGGER.debug("Locking doors for: %s", self.name)
        data = await self._send_command(
            "LOCK",
            path_vars={"vehicle_id": self.car.id},
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            self.car.state["locked"] = True
            self.async_write_ha_state()

    async def async_unlock(self, **kwargs):
        """Send the unlock command."""
        _LOGGER.debug("Unlocking doors for: %s", self.name)
        data = await self._send_command(
            "UNLOCK",
            path_vars={"vehicle_id": self.car.id},
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            self.car.state["locked"] = False
            self.async_write_ha_state()

    @property
    def is_locked(self):
        """Get whether the lock is in locked state."""
        return self.car.state.get("locked")


class ChargerDoor(TeslaCarDevice, LockEntity):
    """Representation of a Tesla Charger door lock."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Lock Entity."""
        super().__init__(hass, car, coordinator)
        self._name = "charger door lock"

    async def async_lock(self, **kwargs):
        """Send the lock command."""
        _LOGGER.debug("Locking doors for: %s", self.name)
        data = await self._send_command(
            "CHARGE_PORT_DOOR_CLOSE",
            path_vars={"vehicle_id": self.car.id},
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            self.car.charging["charge_port_door_open"] = True
            self.async_write_ha_state()

    async def async_unlock(self, **kwargs):
        """Send the unlock command."""
        _LOGGER.debug("Unlocking doors for: %s", self.name)
        data = await self._send_command(
            "CHARGE_PORT_DOOR_OPEN",
            path_vars={"vehicle_id": self.car.id},
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            self.car.charging["charge_port_door_open"] = False
            self.async_write_ha_state()

    @property
    def is_locked(self):
        """Get whether the lock is in locked state."""
        charge_door_open = self.car.charging.get("charge_port_door_open")
        charger_latched = self.car.charging.get("charge_port_latch") == "Engaged"

        if charger_latched:
            return True

        return charge_door_open is False
