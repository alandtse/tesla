"""Support for Tesla selects."""
import logging

from teslajsonpy.car import TeslaCar
from teslajsonpy.energy import PowerwallSite, SolarPowerwallSite
from teslajsonpy.const import RESOURCE_TYPE_BATTERY

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice, TeslaEnergyDevice
from .const import DOMAIN

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

EXPORT_RULE = [
    "Solar",
    "Everything",
]

GRID_CHARGING = [
    "Yes",
    "No",
]

OPERATION_MODE = [
    "Self-Powered",
    "Time-Based Control",
    "Backup",
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
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    energysites = hass.data[DOMAIN][config_entry.entry_id]["energysites"]
    entities = []

    for car in cars.values():
        entities.append(TeslaCabinOverheatProtection(hass, car, coordinator))
        for seat_name in SEAT_ID_MAP:
            if "rear" in seat_name and not car.rear_heated_seats:
                continue
            if "third_row" in seat_name and not car.third_row_seats:
                continue
            entities.append(HeatedSeatSelect(hass, car, coordinator, seat_name))

    for energysite in energysites.values():
        if energysite.resource_type == RESOURCE_TYPE_BATTERY:
            entities.append(TeslaEnergyOperationMode(hass, energysite, coordinator))
        if energysite.resource_type == RESOURCE_TYPE_BATTERY and energysite.has_solar:
            entities.append(TeslaEnergyExportRule(hass, energysite, coordinator))
            entities.append(TeslaEnergyGridCharging(hass, energysite, coordinator))

    async_add_entities(entities, True)


class HeatedSeatSelect(TeslaCarDevice, SelectEntity):
    """Representation of a Tesla Heated Seat Select."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
        seat_name: str,
    ):
        """Initialize a heated seat for the vehicle."""
        super().__init__(hass, car, coordinator)

        self._seat_name = seat_name
        self.type = f"heated seat {seat_name}"

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        level: int = HEATER_OPTIONS.index(option)

        # await wait_for_climate(self.hass, self.config_entry_id)
        _LOGGER.debug("Setting %s to %s", self.name, level)
        await self._car.remote_seat_heater_request(level, SEAT_ID_MAP[self._seat_name])

        await self.update_controller(force=True)

    @property
    def current_option(self):
        """Return the selected entity option to represent the entity state."""
        current_value = self._car.get_seat_heater_status(SEAT_ID_MAP[self._seat_name])

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
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ):
        """Initialize a heated seat for the vehicle."""
        super().__init__(hass, car, coordinator)

        self.type = "cabin overheat protection"
        self._attr_options = CABIN_OPTIONS
        self._attr_entity_category = EntityCategory.CONFIG

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        await self._car.set_cabin_overheat_protection(option)

    @property
    def current_option(self):
        """Return the selected entity option to represent the entity state."""
        return self._car.cabin_overheat_protection


class TeslaEnergyGridCharging(TeslaEnergyDevice, SelectEntity):
    """Representation of a Tesla energy site grid charging."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: SolarPowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ):
        """Initialize grid charging."""
        super().__init__(hass, energysite, coordinator)

        self.type = "grid charging"
        self._attr_options = GRID_CHARGING

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        if option == GRID_CHARGING[0]:
            await self._energysite.set_grid_charging(True)
        else:
            await self._energysite.set_grid_charging(False)

    @property
    def current_option(self):
        """Return the selected entity option to represent the entity state."""
        if self._energysite.grid_charging:
            return GRID_CHARGING[0]
        return GRID_CHARGING[1]


class TeslaEnergyExportRule(TeslaEnergyDevice, SelectEntity):
    """Representation of a Tesla energy site energy export rule."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: SolarPowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ):
        """Initialize operation mode."""
        super().__init__(hass, energysite, coordinator)

        self.type = "energy exports"
        self._attr_options = EXPORT_RULE

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        if option == EXPORT_RULE[0]:
            await self._energysite.set_export_rule("pv_only")
        if option == EXPORT_RULE[1]:
            await self._energysite.set_export_rule("battery_ok")

    @property
    def current_option(self):
        """Return the selected entity option to represent the entity state."""
        if self._energysite.export_rule == "pv_only":
            return EXPORT_RULE[0]
        if self._energysite.export_rule == "battery_ok":
            return EXPORT_RULE[1]


class TeslaEnergyOperationMode(TeslaEnergyDevice, SelectEntity):
    """Representation of a Tesla energy site operation mode."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: PowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ):
        """Initialize operation mode."""
        super().__init__(hass, energysite, coordinator)

        self.type = "operation mode"
        self._attr_options = OPERATION_MODE

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        if option == OPERATION_MODE[0]:
            await self._energysite.set_operation_mode("self_consumption")
        if option == OPERATION_MODE[1]:
            await self._energysite.set_operation_mode("autonomous")
        if option == OPERATION_MODE[2]:
            await self._energysite.set_operation_mode("backup")

    @property
    def current_option(self):
        """Return the selected entity option to represent the entity state."""
        if self._energysite.operation_mode == "self_consumption":
            return OPERATION_MODE[0]
        if self._energysite.operation_mode == "autonomous":
            return OPERATION_MODE[1]
        if self._energysite.operation_mode == "backup":
            return OPERATION_MODE[2]
