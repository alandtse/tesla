"""Support for Tesla device tracker."""
import logging
import math

from teslajsonpy.car import TeslaCar

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.core import HomeAssistant

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity
from .const import AUTH_DOMAIN_CHINA, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla device trackers by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    entities = []

    for car in cars.values():
        entities.append(TeslaCarLocation(hass, car, coordinator))

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
        if (
            str(coordinator.controller._Controller__connection.auth_domain)
            == AUTH_DOMAIN_CHINA
        ):
            self._in_china = True
        else:
            self._in_china = False
        self._location_converter = LocationConverter()

    @property
    def source_type(self):
        """Return device tracker source type."""
        return SOURCE_TYPE_GPS

    @property
    def longitude(self):
        """Return longitude."""
        location = self.location

        if self._in_china:
            location = self._location_converter.gcj02towgs84(location)
            return location.get("longitude)")

        return location.get("longitude")

    @property
    def latitude(self):
        """Return latitude."""
        location = self.location

        if self._in_china:
            location = self._location_converter.gcj02towgs84(location)
            return location.get("latitude)")

        return location.get("latitude")

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        # "native_heading" does not exist in Tesla API with 2015 Model S 85D - newer models only?
        # if self._car.native_location_supported:
        #     heading = self._car.native_heading
        # else:
        #     heading = self._car.heading

        return {
            "heading": self._car.heading,
            "speed": self._car.speed,
        }

    @property
    def force_update(self):
        """Disable forced updated since we are polling via the coordinator updates."""
        return False

    @property
    def location(self) -> dict:
        """Return car location as a dictionary."""
        if self._car.native_location_supported:
            return {
                "longitude": self._car.native_longitude,
                "latitude": self._car.native_latitude,
            }

        return {
            "longitude": self._car.longitude,
            "latitude": self._car.latitude,
        }


class LocationConverter:
    # pylint: disable=invalid-name
    """Convert gcj02 to wgs84 for Chinese users."""

    def __init__(self) -> None:
        """Initialize LocationConverter."""
        self.x_pi = 3.14159265358979324 * 3000.0 / 180.0
        self.pi = 3.1415926535897932384626
        self.a = 6378245.0
        self.ee = 0.00669342162296594323

    def gcj02towgs84(self, location) -> dict:
        """Convert gcj02 to wgs84."""
        lng = location.get("longitude")
        lat = location.get("latitude")
        dlat = self.transform_lat(lng - 105.0, lat - 35.0)
        dlng = self.transform_lng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / (
            (self.a * (1 - self.ee)) / (magic * sqrtmagic) * self.pi
        )
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        location["longitude"] = lng * 2 - mglng
        location["latitude"] = lat * 2 - mglat

        return location

    def transform_lng(self, lng, lat) -> float:
        """Transform longitude."""
        ret = (
            300.0
            + lng
            + 2.0 * lat
            + 0.1 * lng * lng
            + 0.1 * lng * lat
            + 0.1 * math.sqrt(math.fabs(lng))
        )
        ret += (
            (
                20.0 * math.sin(6.0 * lng * self.pi)
                + 20.0 * math.sin(2.0 * lng * self.pi)
            )
            * 2.0
            / 3.0
        )
        ret += (
            (20.0 * math.sin(lng * self.pi) + 40.0 * math.sin(lng / 3.0 * self.pi))
            * 2.0
            / 3.0
        )
        ret += (
            (
                150.0 * math.sin(lng / 12.0 * self.pi)
                + 300.0 * math.sin(lng / 30.0 * self.pi)
            )
            * 2.0
            / 3.0
        )
        return ret

    def transform_lat(self, lng, lat) -> float:
        """Transform latitude."""
        ret = (
            -100.0
            + 2.0 * lng
            + 3.0 * lat
            + 0.2 * lat * lat
            + 0.1 * lng * lat
            + 0.2 * math.sqrt(math.fabs(lng))
        )
        ret += (
            (
                20.0 * math.sin(6.0 * lng * self.pi)
                + 20.0 * math.sin(2.0 * lng * self.pi)
            )
            * 2.0
            / 3.0
        )
        ret += (
            (20.0 * math.sin(lat * self.pi) + 40.0 * math.sin(lat / 3.0 * self.pi))
            * 2.0
            / 3.0
        )
        ret += (
            (
                160.0 * math.sin(lat / 12.0 * self.pi)
                + 320 * math.sin(lat * self.pi / 30.0)
            )
            * 2.0
            / 3.0
        )
        return ret
