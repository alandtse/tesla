"""Support for tracking Tesla cars."""
import logging

from teslajsonpy.car import TeslaCar

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
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
        entities.append(CarLocation(hass, car, coordinator))

    async_add_entities(entities, True)


class CarLocation(TeslaCarDevice, TrackerEntity):
    """Representation of the Tesla Car Location Tracker."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "location tracker"

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def longitude(self):
        """Return longitude value of the device."""
        if self._car.native_location_supported:
            return self._car.native_longitude

        return self._car.longitude

    @property
    def latitude(self):
        """Return latitude value of the device."""
        if self._car.native_location_supported:
            return self._car.native_latitude

        return self._car.latitude

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        if self._car.native_location_supported:
            heading = self._car.native_heading
        else:
            heading = self._car.heading

        attr = {
            "heading": heading,
            "speed": self._car.speed,
        }

        return attr

    @property
    def force_update(self):
        """Disable forced updated since we are polling via the coordinator updates."""
        return False
