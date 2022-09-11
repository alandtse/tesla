"""Support for tracking Tesla cars."""
from __future__ import annotations

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity

from . import DOMAIN as TESLA_DOMAIN
from .tesla_device import TeslaDevice

import math


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Tesla binary_sensors by config_entry."""
    entities = [
        TeslaDeviceEntity(
            device,
            hass.data[TESLA_DOMAIN][config_entry.entry_id]["coordinator"],
        )
        for device in hass.data[TESLA_DOMAIN][config_entry.entry_id]["devices"][
            "devices_tracker"
        ]
    ]
    async_add_entities(entities, True)


class TeslaDeviceEntity(TeslaDevice, TrackerEntity):
    """A class representing a Tesla device."""

    def __init__(self, tesla_device, coordinator):
        super().__init__(tesla_device, coordinator)
        if str(tesla_device._controller._Controller__connection.auth_domain) == "https://auth.tesla.cn":
            self.in_china = True
        else:
            self.in_china = False
        self.location_converter = LocationConverter()

    @property
    def force_update(self):
        """Disable forced updated since we are polling via the coordinator updates."""
        return False

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        location = self.tesla_device.get_location()
        if location and self.in_china:
            location = self.location_converter.gcj02towgs84(location)
        return location.get("latitude") if location else None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        location = self.tesla_device.get_location()
        if location and self.in_china:
            location = self.location_converter.gcj02towgs84(location)
        return location.get("longitude") if location else None

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        attr = super().extra_state_attributes.copy()
        location = self.tesla_device.get_location()
        if location:
            attr.update(
                {
                    "trackr_id": self.unique_id,
                    "heading": location["heading"],
                    "speed": location["speed"],
                }
            )
        return attr


class LocationConverter:
    """Convert gcj02 to wgs84 for Chinese user"""

    def __init__(self):
        self.x_pi = 3.14159265358979324 * 3000.0 / 180.0
        self.pi = 3.1415926535897932384626
        self.a = 6378245.0
        self.ee = 0.00669342162296594323

    def gcj02towgs84(self, location):
        lng = location.get("longitude")
        lat = location.get("latitude")
        dlat = self.transform_lat(lng - 105.0, lat - 35.0)
        dlng = self.transform_lng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        location["longitude"] = lng * 2 - mglng
        location["latitude"] = lat * 2 - mglat
        return location

    def transform_lng(self, lng, lat) -> float:
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 * math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.pi) + 40.0 * math.sin(lng / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.pi) + 300.0 * math.sin(lng / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    def transform_lat(self, lng, lat) -> float:
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 * math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.pi) + 40.0 * math.sin(lat / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.pi) + 320 * math.sin(lat * self.pi / 30.0)) * 2.0 / 3.0
        return ret
