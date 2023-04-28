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
        entities.append(TeslaCarTeslaMateID(hass, car, coordinator, teslamate))

    async_add_entities(entities, update_before_add=True)


class TeslaCarTeslaMateID(TeslaCarEntity, TextEntity):
    """Representation of a Tesla car charge limit number."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
        teslamate: TeslaMate,
    ) -> None:
        """Initialize charge limit entity."""
        super().__init__(hass, car, coordinator)
        self.type = "teslamate id"
        self._attr_icon = "mdi:ev-station"
        self._attr_mode = TextMode.TEXT
        self._enabled_by_default = False
        self._attr_entity_category = EntityCategory.CONFIG

        self.teslsmate = teslamate
        self._state = None

    async def async_set_value(self, value: str) -> None:
        """Update charge limit."""
        if value.strip() == "":
            value = None

        await self.teslsmate.set_car_id(self._car.vin, value)
        await self.teslsmate.watch_cars()
        await self.async_update_ha_state()

    async def async_update(self) -> None:
        """Update the entity."""
        # Ignore manual update requests if the entity is disabled
        self._state = await self.teslsmate.get_car_id(self._car.vin)

    @property
    def native_value(self) -> str:
        """Return charge limit."""
        return self._state
