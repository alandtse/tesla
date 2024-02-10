"""Support for Tesla buttons."""

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from teslajsonpy.car import TeslaCar

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinators = entry_data["coordinators"]
    cars = entry_data["cars"]
    entities = []

    for vin, car in cars.items():
        coordinator = coordinators[vin]
        entities.append(TeslaCarHorn(car, coordinator))
        entities.append(TeslaCarFlashLights(car, coordinator))
        entities.append(TeslaCarWakeUp(car, coordinator))
        entities.append(TeslaCarForceDataUpdate(car, coordinator))
        entities.append(TeslaCarTriggerHomelink(car, coordinator))
        entities.append(TeslaCarRemoteStart(car, coordinator))
        entities.append(TeslaCarEmissionsTest(car, coordinator))

    async_add_entities(entities, update_before_add=True)


class TeslaCarHorn(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car horn button."""

    type = "horn"
    _attr_icon = "mdi:bullhorn"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._car.honk_horn()


class TeslaCarFlashLights(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car flash lights button."""

    type = "flash lights"
    _attr_icon = "mdi:car-light-high"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._car.flash_lights()


class TeslaCarWakeUp(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car wake up button."""

    type = "wake up"
    _attr_icon = "mdi:moon-waning-crescent"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._car.wake_up()

    @property
    def available(self) -> bool:
        """Return True."""
        return True


class TeslaCarForceDataUpdate(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car force data update button."""

    type = "force data update"
    _attr_icon = "mdi:database-sync"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.update_controller(wake_if_asleep=True, force=True)

    @property
    def available(self) -> bool:
        """Return True."""
        return True


class TeslaCarTriggerHomelink(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car Homelink button."""

    type = "homelink"
    _attr_icon = "mdi:garage"

    def __init__(
        self,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialise Homelink button."""
        # Entity is only enabled upon first install if garages have been paired to homelink
        self._enabled_by_default = car.homelink_device_count
        super().__init__(car, coordinator)

    @property
    def available(self) -> bool:
        """Return True if Homelink devices are nearby."""
        return super().available and self._car.homelink_nearby

    async def async_press(self):
        """Send the command."""
        await self._car.trigger_homelink()


class TeslaCarRemoteStart(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car remote start button."""

    type = "remote start"
    _attr_icon = "mdi:power"

    async def async_press(self):
        """Send the command."""
        await self._car.remote_start()


class TeslaCarEmissionsTest(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car emissions test button."""

    type = "emissions test"
    _attr_icon = "mdi:weather-windy"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize emissions test button."""
        self._enabled_by_default = car.pedestrian_speaker
        super().__init__(car, coordinator)

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._car.remote_boombox()

    @property
    def available(self) -> bool:
        """Return True."""
        return True
