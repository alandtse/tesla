"""Support for Tesla device tracker."""
import logging

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.core import HomeAssistant
from teslajsonpy.car import TeslaCar

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla device trackers by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    entities = []

    for car in cars.values():
        entities.append(TeslaCarLocation(hass, car, coordinator))
        entities.append(TeslaCarDestinationLocation(hass, car, coordinator))

    async_add_entities(entities, True)


class TeslaCarLocation(TeslaCarEntity, TrackerEntity):
    """Representation of a Tesla car location device tracker."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize car location entity."""
        super().__init__(hass, car, coordinator)
        self.type = "location tracker"

    @property
    def source_type(self):
        """Return device tracker source type."""
        return SOURCE_TYPE_GPS

    @property
    def longitude(self):
        """Return longitude."""
        return self._car.longitude

    @property
    def latitude(self):
        """Return latitude."""
        return self._car.latitude

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "heading": self._car.heading,
            "speed": self._car.speed,
        }

    @property
    def force_update(self):
        """Disable forced updated since we are polling via the coordinator updates."""
        return False


class TeslaCarDestinationLocation(TeslaCarEntity, TrackerEntity):
    """Representation of a Tesla car destination location device tracker."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize car destination location entity."""
        super().__init__(hass, car, coordinator)
        self.type = "destination location tracker"

    @property
    def source_type(self):
        """Return device tracker source type."""
        return SOURCE_TYPE_GPS

    @property
    def longitude(self):
        """Return destination longitude."""
        if self._car.active_route_miles_to_arrival is None:
            return None
        return self._car.active_route_longitude

    @property
    def latitude(self):
        """Return destination latitude."""
        if self._car.active_route_miles_to_arrival is None:
            return None
        return self._car.active_route_latitude

    @property
    def force_update(self):
        """Disable forced updated since we are polling via the coordinator updates."""
        return False
