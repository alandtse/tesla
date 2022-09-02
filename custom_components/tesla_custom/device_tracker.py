"""Support for Tesla device tracker."""
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
    """Set up the Tesla device trackers by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    entities = []

    for car in cars.values():
        entities.append(CarLocation(hass, car, coordinator))

    async_add_entities(entities, True)


class CarLocation(TeslaCarDevice, TrackerEntity):
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
        if self._car.native_location_supported:
            return self._car.native_longitude

        return self._car.longitude

    @property
    def latitude(self):
        """Return latitude."""
        if self._car.native_location_supported:
            return self._car.native_latitude

        return self._car.latitude

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        # "native_heading" does not exist in Tesla API with 2015 Model S 85D - newer models only?
        # if self._car.native_location_supported:
        #     heading = self._car.native_heading
        # else:
        #     heading = self._car.heading

        attr = {
            "heading": self._car.heading,
            "speed": self._car.speed,
        }

        return attr

    @property
    def force_update(self):
        """Disable forced updated since we are polling via the coordinator updates."""
        return False
