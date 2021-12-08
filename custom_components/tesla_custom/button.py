"""Support for Tesla charger buttons."""
from custom_components.tesla_custom.const import ICONS
import logging

_LOGGER = logging.getLogger(__name__)

from homeassistant.components.button import ButtonEntity

from . import DOMAIN as TESLA_DOMAIN
from .tesla_device import TeslaDevice


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Tesla button by config_entry."""
    coordinator = hass.data[TESLA_DOMAIN][config_entry.entry_id]["coordinator"]
    entities = []
    for device in hass.data[TESLA_DOMAIN][config_entry.entry_id]["devices"]["button"]:
        if device.type == "horn":
            entities.append(Horn(device, coordinator))
        elif device.type == "flash lights":
            entities.append(FlashLights(device, coordinator))
    async_add_entities(entities, True)


class Horn(TeslaDevice, ButtonEntity):
    """Representation of a Tesla horn button."""

    def __init__(self, tesla_device, coordinator):
        """Initialise the button."""
        super().__init__(tesla_device, coordinator)
        self.controller = coordinator.controller

    @TeslaDevice.Decorators.check_for_reauth
    async def async_press(self, **kwargs):
        """Send the command."""
        _LOGGER.debug("Honk horn: %s", self.name)
        await self.tesla_device.honk_horn()


class FlashLights(TeslaDevice, ButtonEntity):
    """Representation of a Tesla flash lights button."""

    def __init__(self, tesla_device, coordinator):
        """Initialise the button."""
        super().__init__(tesla_device, coordinator)
        self.controller = coordinator.controller

    @TeslaDevice.Decorators.check_for_reauth
    async def async_press(self, **kwargs):
        """Send the command."""
        _LOGGER.debug("Flash lights: %s", self.name)
        await self.tesla_device.flash_lights()
