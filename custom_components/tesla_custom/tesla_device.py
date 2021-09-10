"""Support for Tesla cars."""
import logging

from homeassistant.const import ATTR_BATTERY_CHARGING, ATTR_BATTERY_LEVEL
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import DOMAIN, ICONS

_LOGGER = logging.getLogger(__name__)


class TeslaDevice(CoordinatorEntity):
    """Representation of a Tesla device."""

    def __init__(self, tesla_device, coordinator):
        """Initialise the Tesla device."""
        super().__init__(coordinator)
        self.tesla_device = tesla_device
        self._name = self.tesla_device.name
        self._unique_id = slugify(self.tesla_device.uniq_name)
        self._attributes = self.tesla_device.attrs.copy()

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._unique_id

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if self.device_class:
            return None

        return ICONS.get(self.tesla_device.type)

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        attr = self._attributes
        if self.tesla_device.has_battery():
            attr[ATTR_BATTERY_LEVEL] = self.tesla_device.battery_level()
            attr[ATTR_BATTERY_CHARGING] = self.tesla_device.battery_charging()
        return attr

    @property
    def device_info(self):
        """Return the device_info of the device."""
        return {
            "identifiers": {(DOMAIN, self.tesla_device.id())},
            "name": self.tesla_device.car_name(),
            "manufacturer": "Tesla",
            "model": self.tesla_device.car_type,
            "sw_version": self.tesla_device.car_version,
        }

    async def async_added_to_hass(self):
        """Register state update callback."""
        self.async_on_remove(self.coordinator.async_add_listener(self.refresh))

    @callback
    def refresh(self) -> None:
        """Refresh the state of the device.

        This assumes the coordinator has updated the controller.
        """
        self.tesla_device.refresh()
        self._attributes = self.tesla_device.attrs.copy()
        self.async_write_ha_state()
