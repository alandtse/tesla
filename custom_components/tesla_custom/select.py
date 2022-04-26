"""Support for Tesla selects."""
import logging

from homeassistant.components.select import SelectEntity

from .const import DOMAIN
from .base import TeslaBaseEntity
from . import TeslaDataUpdateCoordinator
from .helpers import wait_for_climate

_LOGGER = logging.getLogger(__name__)

OPTIONS = [
    "Off",
    "Low",
    "Medium",
    "High",
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


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    entities = []
    for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]:
        for seat_name in SEAT_ID_MAP.keys():
            entities.append(HeatedSeatSelect(car, coordinator, seat_name))

    async_add_entities(entities, True)


class HeatedSeatSelect(TeslaBaseEntity, SelectEntity):
    """Representation of a Tesla Heated Seat Select."""

    def __init__(
        self, car: dict, coordinator: TeslaDataUpdateCoordinator, seat_name: str
    ):
        """Initialize a heated seat for the vehicle."""
        super().__init__(car, coordinator)

        self._seat_name = seat_name
        self.type = f"heated seat {seat_name}"

        # For 3rd row disable by default
        if self._seat_name in ["third_row_left", "third_row_right"]:
            self._enabled_by_default = False

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        level: int = OPTIONS.index(option)

        # await wait_for_climate(self.hass, self.config_entry_id)
        _LOGGER.debug("Setting %s to %s", self.name, level)
        data = await self._coordinator.controller.api(
            "REMOTE_SEAT_HEATER_REQUEST",
            path_vars={"vehicle_id": self.car.id},
            heater=SEAT_ID_MAP[self._seat_name],
            level=level,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            self.car.climate[self._seat_key] = level

        self.async_write_ha_state()

    @property
    def current_option(self):
        """Return the selected entity option to represent the entity state."""
        current_value = self.car.climate.get(self._seat_key)

        if current_value is None:
            return OPTIONS[0]
        return OPTIONS[current_value]

    @property
    def _seat_key(self):
        return f"seat_heater_{self._seat_name}"

    @property
    def options(self):
        """Return a set of selectable options."""
        return OPTIONS
