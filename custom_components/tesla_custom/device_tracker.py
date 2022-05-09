"""Support for tracking Tesla cars."""
import logging

from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.helpers.entity import EntityCategory


from homeassistant.core import HomeAssistant

from . import TeslaDataUpdateCoordinator
from .base import TeslaBaseEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities = []
    for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]:
        entities.append(CarLocation(hass, car, coordinator))

    async_add_entities(entities, True)


class CarLocation(TeslaBaseEntity, TrackerEntity):
    """Representation of the Tesla Car Location Tracker."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "location tracker"

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        data: dict = self.car.drive
        if data.get("native_location_supported"):
            return data.get("native_longitude")

        return data.get("longitude")

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        data: dict = self.car.drive
        if data.get("native_location_supported"):
            return data.get("native_latitude")

        return data.get("latitude")

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        data: dict = self.car.drive
        if data.get("native_location_supported"):
            heading = data.get("native_heading")
        else:
            heading = data.get("heading")

        attr = {
            "heading": heading,
            "speed": data.get("speed", 0),
        }

        return attr

    @property
    def force_update(self):
        """Disable forced updated since we are polling via the coordinator updates."""
        return False
