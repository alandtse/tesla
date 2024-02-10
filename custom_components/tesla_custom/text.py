"""Support for Tesla numbers."""

from homeassistant.components.text import TextEntity, TextMode
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from teslajsonpy.car import TeslaCar

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity
from .const import DOMAIN
from .teslamate import TeslaMate


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla numbers by config_entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinators = entry_data["coordinators"]
    cars = entry_data["cars"]
    teslamate = entry_data["teslamate"]
    entities = []

    for vin, car in cars.items():
        coordinator = coordinators[vin]
        entities.append(TeslaCarTeslaMateID(car, coordinator, teslamate))

    async_add_entities(entities, update_before_add=True)


class TeslaCarTeslaMateID(TeslaCarEntity, TextEntity):
    """Representation of a Tesla car charge limit number."""

    type = "teslamate id"
    _attr_icon = "mdi:ev-station"
    _attr_mode = TextMode.TEXT
    _enabled_by_default = False
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
        teslamate: TeslaMate,
    ) -> None:
        """Initialize charge limit entity."""
        self.teslamate = teslamate
        self._state = None
        super().__init__(car, coordinator)

    async def async_set_value(self, value: str) -> None:
        """Update charge limit."""
        if value.strip() == "":
            value = None

        await self.teslamate.set_car_id(self._car.vin, value)
        await self.teslamate.watch_cars()
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update the entity."""
        # Ignore manual update requests if the entity is disabled
        self._state = await self.teslamate.get_car_id(self._car.vin)

    @property
    def native_value(self) -> str:
        """Return charge limit."""
        return self._state
