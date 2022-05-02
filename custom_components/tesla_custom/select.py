"""Support for Tesla selects."""
import logging

from homeassistant.components.select import SelectEntity

from . import DOMAIN as TESLA_DOMAIN
from .tesla_device import TeslaDevice
from .helpers import wait_for_climate

_LOGGER = logging.getLogger(__name__)

OPTIONS = [
    "Off",
    "Low",
    "Medium",
    "High",
]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    coordinator = hass.data[TESLA_DOMAIN][config_entry.entry_id]["coordinator"]
    entities = []
    for device in hass.data[TESLA_DOMAIN][config_entry.entry_id]["devices"]["select"]:
        if device.type.startswith("heated seat "):
            entities.append(HeatedSeatSelect(device, coordinator))
    async_add_entities(entities, True)


class HeatedSeatSelect(TeslaDevice, SelectEntity):
    """Representation of a Tesla Heated Seat Select."""

    @TeslaDevice.Decorators.check_for_reauth
    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        level: int = OPTIONS.index(option)

        vin = self.tesla_device.vin()
        await wait_for_climate(self.hass, self.config_entry_id, vin)
        _LOGGER.debug("Setting %s to %s", self.name, level)
        await self.tesla_device.set_seat_heat_level(level)
        self.async_write_ha_state()

    @property
    def current_option(self):
        """Return the selected entity option to represent the entity state."""
        current_value = self.tesla_device.get_seat_heat_level()

        if current_value is None:
            return OPTIONS[0]
        return OPTIONS[current_value]

    @property
    def options(self):
        """Return a set of selectable options."""
        return OPTIONS
