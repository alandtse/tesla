"""Support for Tesla selects."""
import logging

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice
from .const import DOMAIN
from .helpers import wait_for_climate

_LOGGER = logging.getLogger(__name__)

HEATER_OPTIONS = [
    "Off",
    "Low",
    "Medium",
    "High",
]

CABIN_OPTIONS = [
    "Off",
    "No A/C",
    "On",
]

SEAT_ID_MAP = {
    "left": 0,
    "right": 1,
    "rear_left": 2,
    "rear_center": 4,
    "rear_right": 5,
    "third_row_left": 6,
    "third_row_right": 7,
}


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    entities = []
    for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]:
        entities.append(TeslaCabinOverheatProtection(hass, car, coordinator))

        for seat_name in SEAT_ID_MAP:
            entities.append(HeatedSeatSelect(hass, car, coordinator, seat_name))

    async_add_entities(entities, True)


class HeatedSeatSelect(TeslaCarDevice, SelectEntity):
    """Representation of a Tesla Heated Seat Select."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: dict,
        coordinator: TeslaDataUpdateCoordinator,
        seat_name: str,
    ):
        """Initialize a heated seat for the vehicle."""
        super().__init__(hass, car, coordinator)

        self._seat_name = seat_name
        self._name = f"heated seat {seat_name}"

        # For 3rd row disable by default
        if (
            self._seat_name in ["third_row_left", "third_row_right"]
            and self.car.config.get("third_row_seats") is not None
        ):
            self._enabled_by_default = False

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        level: int = HEATER_OPTIONS.index(option)

        # await wait_for_climate(self.hass, self.config_entry_id)
        _LOGGER.debug("Setting %s to %s", self.name, level)
        data = await self._send_command(
            "REMOTE_SEAT_HEATER_REQUEST",
            path_vars={"vehicle_id": self.car.id},
            heater=SEAT_ID_MAP[self._seat_name],
            level=level,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            self.car.climate[self._seat_key] = level

        await self.update_controller(force=True)
        self.async_write_ha_state()

    @property
    def current_option(self):
        """Return the selected entity option to represent the entity state."""
        current_value = self.car.climate.get(self._seat_key)

        if current_value is None:
            return HEATER_OPTIONS[0]
        return HEATER_OPTIONS[current_value]

    @property
    def _seat_key(self):
        return f"seat_heater_{self._seat_name}"

    @property
    def options(self):
        """Return a set of selectable options."""
        return HEATER_OPTIONS


class TeslaCabinOverheatProtection(TeslaCarDevice, SelectEntity):
    """Representation of a Tesla Heated Seat Select."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: dict,
        coordinator: TeslaDataUpdateCoordinator,
    ):
        """Initialize a heated seat for the vehicle."""
        super().__init__(hass, car, coordinator)

        self._name = "cabin overheat protection"
        self._attr_options = CABIN_OPTIONS
        self._attr_entity_category = EntityCategory.CONFIG

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""

        if option == "Off":
            body_on = False
            fan_only = False
        elif option == "No A/C":
            body_on = True
            fan_only = True
        elif option == "On":
            body_on = True
            fan_only = False

        data = await self._send_command(
            "SET_CABIN_OVERHEAT_PROTECTION",
            path_vars={"vehicle_id": self.car.id},
            on=body_on,
            fan_only=fan_only,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            self.car.climate["cabin_overheat_protection"] = option
            self.async_write_ha_state()

    @property
    def current_option(self):
        """Return the selected entity option to represent the entity state."""
        return self.car.climate.get("cabin_overheat_protection")
