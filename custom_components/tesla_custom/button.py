"""Support for Tesla charger buttons."""
import logging

from teslajsonpy.car import TeslaCar
from teslajsonpy.exceptions import HomelinkError

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory

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
        entities.append(Horn(hass, car, coordinator))
        entities.append(FlashLights(hass, car, coordinator))
        entities.append(WakeUp(hass, car, coordinator))
        entities.append(ForceDataUpdate(hass, car, coordinator))
        entities.append(TriggerHomelink(hass, car, coordinator))

    async_add_entities(entities, True)


class Horn(TeslaCarDevice, ButtonEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "horn"
        self._attr_icon = "mdi:bullhorn"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._car.honk_horn()


class FlashLights(TeslaCarDevice, ButtonEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "flash lights"
        self._attr_icon = "mdi:car-light-high"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._car.flash_lights()


class WakeUp(TeslaCarDevice, ButtonEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "wake up"
        self._attr_icon = "mdi:moon-waning-crescent"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._car.wake_up()


class ForceDataUpdate(TeslaCarDevice, ButtonEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "force Data update"
        self._attr_icon = "mdi:database-sync"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.update_controller(wake_if_asleep=True, force=True)

    @property
    def available(self) -> bool:
        """Return True."""
        return True


class TriggerHomelink(TeslaCarDevice, ButtonEntity):
    """Representation of a Tesla Homelink button."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialise the button."""
        super().__init__(hass, car, coordinator)
        self.type = "trigger homelink"
        self._attr_icon = "mdi:garage"
        self.__waiting = False
        self._enabled_by_default = False

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and not self.__waiting

    async def async_press(self, **kwargs):
        """Send the command."""
        self.__waiting = True
        self.async_write_ha_state()
        try:
            await self.update_controller(wake_if_asleep=True, force=True, blocking=True)
            await self._car.trigger_homelink()
        except HomelinkError as ex:
            _LOGGER.error("%s", ex.message)
        finally:
            self.__waiting = False
            self.async_write_ha_state()
