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
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    entities = []

    for car in cars.values():
        entities.append(TeslaCarHorn(hass, car, coordinator))
        entities.append(TeslaCarFlashLights(hass, car, coordinator))
        entities.append(TeslaCarWakeUp(hass, car, coordinator))
        entities.append(TeslaCarForceDataUpdate(hass, car, coordinator))
        entities.append(TeslaCarTriggerHomelink(hass, car, coordinator))
        entities.append(TeslaCarRemoteStart(hass, car, coordinator))
        entities.append(TeslaCarEmissionsTest(hass, car, coordinator))

    async_add_entities(entities, True)


class TeslaCarHorn(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car horn button."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize horn entity."""
        super().__init__(hass, car, coordinator)
        self.type = "horn"
        self._attr_icon = "mdi:bullhorn"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._car.honk_horn()


class TeslaCarFlashLights(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car flash lights button."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize flash light entity."""
        super().__init__(hass, car, coordinator)
        self.type = "flash lights"
        self._attr_icon = "mdi:car-light-high"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._car.flash_lights()


class TeslaCarWakeUp(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car wake up button."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize wake up button."""
        super().__init__(hass, car, coordinator)
        self.type = "wake up"
        self._attr_icon = "mdi:moon-waning-crescent"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._car.wake_up()

    @property
    def available(self) -> bool:
        """Return True."""
        return True


class TeslaCarForceDataUpdate(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car force data update button."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize force data update button."""
        super().__init__(hass, car, coordinator)
        self.type = "force data update"
        self._attr_icon = "mdi:database-sync"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.update_controller(wake_if_asleep=True, force=True)

    @property
    def available(self) -> bool:
        """Return True."""
        return True


class TeslaCarTriggerHomelink(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car Homelink button."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialise Homelink button."""
        super().__init__(hass, car, coordinator)
        self.type = "homelink"
        self._attr_icon = "mdi:garage"
        # Entity is only enabled upon first install if garages have been paired to homelink
        self._enabled_by_default = self._car.homelink_device_count

    @property
    def available(self) -> bool:
        """Return True if Homelink devices are nearby."""
        return super().available and self._car.homelink_nearby

    async def async_press(self):
        """Send the command."""
        await self._car.trigger_homelink()


class TeslaCarRemoteStart(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car remote start button."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialise remote start button."""
        super().__init__(hass, car, coordinator)
        self.type = "remote start"
        self._attr_icon = "mdi:power"

    async def async_press(self):
        """Send the command."""
        await self._car.remote_start()


class TeslaCarEmissionsTest(TeslaCarEntity, ButtonEntity):
    """Representation of a Tesla car emissions test button."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize emissions test button."""
        super().__init__(hass, car, coordinator)
        self.type = "emissions test"
        self._attr_icon = "mdi:weather-windy"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._enabled_by_default = self._car.pedestrian_speaker

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._car.remote_boombox()

    @property
    def available(self) -> bool:
        """Return True."""
        return True
