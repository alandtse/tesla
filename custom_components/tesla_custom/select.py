"""Support for Tesla selects."""

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from teslajsonpy.car import TeslaCar
from teslajsonpy.const import RESOURCE_TYPE_BATTERY

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity, TeslaEnergyEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CABIN_OPTIONS = [
    "Off",
    "No A/C",
    "On",
]

EXPORT_RULE = [
    "Nothing",
    "Solar",
    "Everything",
]

GRID_CHARGING = [
    "Yes",
    "No",
]

HEATER_OPTIONS = [
    "Off",
    "Low",
    "Medium",
    "High",
]

FRONT_HEATER_OPTIONS = [
    "Off",
    "Low",
    "Medium",
    "High",
    "Auto",
]

FRONT_COOL_HEAT_OPTIONS = [
    "Off",
    "Heat Low",
    "Heat Medium",
    "Heat High",
    "Auto",
    "Cool Low",
    "Cool Medium",
    "Cool High",
]

STEERING_HEATER_OPTIONS = [
    "Off",
    "Low",
    "High",
    "Auto",
]

STEERING_HEATER_OPTIONS_MAP = {"Off": 0, "Low": 1, "High": 3}

OPERATION_MODE = [
    "Self-Powered",
    "Time-Based Control",
    "Backup",
]

SEAT_ID_MAP = {
    "left": 0,
    "right": 1,
    "rear left": 2,
    "rear center": 4,
    "rear right": 5,
    "third row left": 6,
    "third row right": 7,
}

# Also used by cooled seats
AUTO_SEAT_ID_MAP = {
    "left": 1,
    "right": 2,
}


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinators = entry_data["coordinators"]
    cars = entry_data["cars"]
    energysites = entry_data["energysites"]
    entities = []

    for vin, car in cars.items():
        coordinator = coordinators[vin]
        entities.append(TeslaCarCabinOverheatProtection(car, coordinator))
        if car.get_heated_steering_wheel_level() is not None:
            # Only add steering wheel select if we have a variable heated steering wheel
            entities.append(TeslaCarHeatedSteeringWheel(car, coordinator))
        for seat_name in SEAT_ID_MAP:
            if "rear" in seat_name and not car.rear_seat_heaters:
                continue
            # Check for str "None" (car does not have third row seats)
            # or None (car is asleep)
            if "third" in seat_name and (
                car.third_row_seats == "None" or car.third_row_seats is None
            ):
                continue
            _LOGGER.debug("Setting up seat %s.", seat_name)
            entities.append(TeslaCarHeatedSeat(car, coordinator, seat_name))

    for energy_site_id, energysite in energysites.items():
        coordinator = coordinators[energy_site_id]
        if energysite.resource_type == RESOURCE_TYPE_BATTERY:
            entities.append(TeslaEnergyOperationMode(energysite, coordinator))
        if energysite.resource_type == RESOURCE_TYPE_BATTERY and energysite.has_solar:
            entities.append(TeslaEnergyExportRule(energysite, coordinator))
            entities.append(TeslaEnergyGridCharging(energysite, coordinator))

    async_add_entities(entities, update_before_add=True)


class TeslaCarHeatedSeat(TeslaCarEntity, SelectEntity):
    """Representation of a Tesla car heated/cooling seat select."""

    _attr_icon = "mdi:car-seat-heater"

    def __init__(
        self,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
        seat_name: str,
    ):
        """Initialize heated/cooling seat entity."""
        self._seat_name = seat_name
        self.type = f"heated seat {seat_name}"
        if SEAT_ID_MAP[self._seat_name] < 2:
            self._is_auto_available = True
        else:
            self._is_auto_available = False
        super().__init__(car, coordinator)

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        # If selected auto
        if self._is_auto_available and option == FRONT_HEATER_OPTIONS[4]:
            _LOGGER.debug("Setting %s to %s", self.name, option)
            await self._car.remote_auto_seat_climate_request(
                AUTO_SEAT_ID_MAP[self._seat_name], True
            )
        # If any options other than auto
        else:
            # First turn off auto if currently on
            if self.current_option == FRONT_HEATER_OPTIONS[4]:
                _LOGGER.debug("Turning off Auto heat/cool on %s", self.name)
                await self._car.remote_auto_seat_climate_request(
                    AUTO_SEAT_ID_MAP[self._seat_name], False
                )
            # If front seat and car has seat cooling
            if self._is_auto_available and self._car.has_seat_cooling:
                level: int = FRONT_COOL_HEAT_OPTIONS.index(option)
                if not self._car.is_climate_on and level > 0:
                    await self._car.set_hvac_mode("on")
                # If turning off
                if option == FRONT_COOL_HEAT_OPTIONS[0]:
                    _LOGGER.debug("Turning off Cooling/%s", self.name)
                    # If auto, turn off both heat and cool
                    if getattr(self._car, "is_auto_seat_climate_" + self._seat_name):
                        _LOGGER.debug(
                            "Currently on Auto, Turning off Both heat and cooling on Cooling/%s",
                            self.name,
                        )
                        await self._car.remote_seat_heater_request(
                            level, SEAT_ID_MAP[self._seat_name]
                        )
                        await self._car.remote_seat_cooler_request(
                            1, AUTO_SEAT_ID_MAP[self._seat_name]
                        )
                    # If heating, turn off heat
                    elif self._car.get_seat_heater_status(SEAT_ID_MAP[self._seat_name]):
                        _LOGGER.debug("Turning off heat on Cooling/%s", self.name)
                        await self._car.remote_seat_heater_request(
                            level, SEAT_ID_MAP[self._seat_name]
                        )
                    # If cooling, turn off cooling, 1 is off
                    else:
                        _LOGGER.debug("Turning off cooling on Cooling/%s", self.name)
                        await self._car.remote_seat_cooler_request(
                            1, AUTO_SEAT_ID_MAP[self._seat_name]
                        )
                # If heat levels selected
                elif "Heat" in option:
                    _LOGGER.debug("Setting Cooling/%s to heat %s", self.name, level)
                    await self._car.remote_seat_heater_request(
                        level, SEAT_ID_MAP[self._seat_name]
                    )
                # If cool levels selected
                elif "Cool" in option:
                    # Cool Low == 2, Cool Medium == 3, Cool High ==4
                    level = level - (FRONT_COOL_HEAT_OPTIONS.index("Cool Low") - 2)
                    _LOGGER.debug("Setting Cooling/%s to cool %s", self.name, level)
                    await self._car.remote_seat_cooler_request(
                        level, AUTO_SEAT_ID_MAP[self._seat_name]
                    )
            # If no seat cooling and not setting to auto
            else:
                level: int = HEATER_OPTIONS.index(option)
                if not self._car.is_climate_on and level > 0:
                    await self._car.set_hvac_mode("on")
                _LOGGER.debug("Setting %s to %s", self.name, level)
                await self._car.remote_seat_heater_request(
                    level, SEAT_ID_MAP[self._seat_name]
                )

        await self.update_controller(force=True)

    @property
    def current_option(self):
        """Return current heated/cooling seat setting."""
        # If front seats and auto
        if self._is_auto_available and getattr(
            self._car, "is_auto_seat_climate_" + self._seat_name
        ):
            current_value = 4
            _LOGGER.debug(
                "Current setting for %s is %s",
                self._seat_name,
                FRONT_HEATER_OPTIONS[current_value],
            )
            return FRONT_HEATER_OPTIONS[current_value]
        # If front seats and car has heated/cooling seats
        if self._is_auto_available and self._car.has_seat_cooling:
            current_value = self._car.get_seat_heater_status(
                SEAT_ID_MAP[self._seat_name]
            )
            if current_value is None:
                current_value = self._car.get_seat_cooler_status(
                    AUTO_SEAT_ID_MAP[self._seat_name]
                )
                # Cooling seat level 1 is off
                if current_value == 1:
                    current_value = 0
                else:
                    # Cool Low is 2 but is item 5 on select list
                    current_value = current_value + (
                        FRONT_COOL_HEAT_OPTIONS.index("Cool Low") - 2
                    )
            _LOGGER.debug(
                "Current setting for Cooling/%s is %s",
                self._seat_name,
                FRONT_COOL_HEAT_OPTIONS[current_value],
            )
            return FRONT_COOL_HEAT_OPTIONS[current_value]
        # If front seats w/o cooling seats, or if rear seats
        if (
            self._is_auto_available and not self._car.has_seat_cooling
        ) or "rear" in self._seat_name:
            current_value = self._car.get_seat_heater_status(
                SEAT_ID_MAP[self._seat_name]
            )
            # If heater is off
            if current_value is None:
                current_value = 0

            _LOGGER.debug(
                "Current setting for %s is %s",
                self._seat_name,
                HEATER_OPTIONS[current_value],
            )
            return HEATER_OPTIONS[current_value]

    @property
    def options(self):
        """Return heated seat options."""
        if self._car.has_seat_cooling and self._is_auto_available:
            return FRONT_COOL_HEAT_OPTIONS
        elif self._is_auto_available:
            return FRONT_HEATER_OPTIONS
        else:
            return HEATER_OPTIONS


class TeslaCarHeatedSteeringWheel(TeslaCarEntity, SelectEntity):
    """Representation of a Tesla car heated steering wheel select."""

    type = "heated steering wheel"
    _attr_icon = "mdi:steering"

    def __init__(
        self,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ):
        """Initialize heated steering wheel entity."""
        self._enabled_by_default = car.steering_wheel_heater
        super().__init__(car, coordinator)

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""

        if option == STEERING_HEATER_OPTIONS[3]:
            _LOGGER.debug("Setting Heated Steering to Auto")
            await self._car.remote_auto_steering_wheel_heat_climate_request(True)
        else:
            level: int = STEERING_HEATER_OPTIONS_MAP[option]

            await self._car.remote_auto_steering_wheel_heat_climate_request(False)

            if not self._car.is_climate_on and level > 0:
                await self._car.set_hvac_mode("on")

            _LOGGER.debug("Setting Heated Steering to %s", level)
            await self._car.set_heated_steering_wheel_level(level)

        await self.update_controller(force=True)

    @property
    def current_option(self):
        """Return current heated steering setting."""
        if self._car.is_auto_steering_wheel_heat is True:
            current_str = "Auto"
        else:
            current_value = self._car.get_heated_steering_wheel_level()
            current_str = next(
                (
                    key
                    for key, val in STEERING_HEATER_OPTIONS_MAP.items()
                    if val == current_value
                ),
                None,
            )

        options_idx = STEERING_HEATER_OPTIONS.index(current_str)

        return STEERING_HEATER_OPTIONS[options_idx]

    @property
    def options(self):
        """Return heated steering wheel options."""
        return STEERING_HEATER_OPTIONS

    @property
    def available(self) -> bool:
        """Return True if steering wheel heater is available."""
        return super().available and self._car.steering_wheel_heater


class TeslaCarCabinOverheatProtection(TeslaCarEntity, SelectEntity):
    """Representation of a Tesla car cabin overheat protection select."""

    type = "cabin overheat protection"
    _attr_options = CABIN_OPTIONS
    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:sun-thermometer"

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        await self._car.set_cabin_overheat_protection(option)
        self.async_write_ha_state()

    @property
    def current_option(self):
        """Return current cabin overheat protection setting."""
        return self._car.cabin_overheat_protection


class TeslaEnergyGridCharging(TeslaEnergyEntity, SelectEntity):
    """Representation of a Tesla energy site grid charging select."""

    type = "grid charging"
    _attr_options = GRID_CHARGING

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        if option == GRID_CHARGING[0]:
            await self._energysite.set_grid_charging(True)
        else:
            await self._energysite.set_grid_charging(False)

        self.async_write_ha_state()

    @property
    def current_option(self):
        """Return current grid charging setting."""
        if self._energysite.grid_charging:
            return GRID_CHARGING[0]
        return GRID_CHARGING[1]

    @property
    def icon(self):
        """Return icon for the grid charging."""
        if self._energysite.grid_charging:
            return "mdi:transmission-tower-export"
        return "mdi:transmission-tower-off"


class TeslaEnergyExportRule(TeslaEnergyEntity, SelectEntity):
    """Representation of a Tesla energy site energy export rule select."""

    type = "energy exports"
    _attr_options = EXPORT_RULE
    _attr_icon = "mdi:home-export-outline"

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        if option == EXPORT_RULE[0]:
            await self._energysite.set_export_rule("never")
        if option == EXPORT_RULE[1]:
            await self._energysite.set_export_rule("pv_only")
        if option == EXPORT_RULE[2]:
            await self._energysite.set_export_rule("battery_ok")

        self.async_write_ha_state()

    @property
    def current_option(self) -> str:
        """Return current energy export rule setting."""
        if self._energysite.export_rule == "never":
            return EXPORT_RULE[0]
        if self._energysite.export_rule == "pv_only":
            return EXPORT_RULE[1]
        if self._energysite.export_rule == "battery_ok":
            return EXPORT_RULE[2]
        return ""


class TeslaEnergyOperationMode(TeslaEnergyEntity, SelectEntity):
    """Representation of a Tesla energy site operation mode select."""

    type = "operation mode"
    _attr_options = OPERATION_MODE
    _attr_icon = "mdi:home-battery"

    async def async_select_option(self, option: str, **kwargs):
        """Change the selected option."""
        if option == OPERATION_MODE[0]:
            await self._energysite.set_operation_mode("self_consumption")
        if option == OPERATION_MODE[1]:
            await self._energysite.set_operation_mode("autonomous")
        if option == OPERATION_MODE[2]:
            await self._energysite.set_operation_mode("backup")

        self.async_write_ha_state()

    @property
    def current_option(self) -> str:
        """Return current operation mode setting."""
        if self._energysite.operation_mode == "self_consumption":
            return OPERATION_MODE[0]
        if self._energysite.operation_mode == "autonomous":
            return OPERATION_MODE[1]
        if self._energysite.operation_mode == "backup":
            return OPERATION_MODE[2]
        return ""
