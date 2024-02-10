"""Support for Tesla binary sensors."""

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from teslajsonpy.const import GRID_ACTIVE, RESOURCE_TYPE_BATTERY

from .base import TeslaCarEntity, TeslaEnergyEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinators = entry_data["coordinators"]
    cars = entry_data["cars"]
    energysites = entry_data["energysites"]
    entities = []

    for vin, car in cars.items():
        coordinator = coordinators[vin]
        entities.append(TeslaCarParkingBrake(car, coordinator))
        entities.append(TeslaCarOnline(car, coordinator))
        entities.append(TeslaCarAsleep(car, coordinator))
        entities.append(TeslaCarChargerConnection(car, coordinator))
        entities.append(TeslaCarCharging(car, coordinator))
        entities.append(TeslaCarDoors(car, coordinator))
        entities.append(TeslaCarWindows(car, coordinator))
        entities.append(TeslaCarScheduledCharging(car, coordinator))
        entities.append(TeslaCarScheduledDeparture(car, coordinator))
        entities.append(TeslaCarUserPresent(car, coordinator))

    for energy_site_id, energysite in energysites.items():
        coordinator = coordinators[energy_site_id]
        if energysite.resource_type == RESOURCE_TYPE_BATTERY:
            entities.append(TeslaEnergyBatteryCharging(energysite, coordinator))
            entities.append(TeslaEnergyGridStatus(energysite, coordinator))

    async_add_entities(entities, update_before_add=True)


class TeslaCarParkingBrake(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car parking brake binary sensor."""

    type = "parking brake"
    _attr_icon = "mdi:car-brake-parking"
    _attr_device_class = None

    @property
    def is_on(self):
        """Return True if car shift state in park or None."""
        # When car is parked and off, Tesla API reports shift_state None
        return self._car.shift_state == "P" or self._car.shift_state is None


class TeslaCarChargerConnection(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car charger connection binary sensor."""

    type = "charger"
    _attr_icon = "mdi:ev-station"
    _attr_device_class = BinarySensorDeviceClass.PLUG

    @property
    def is_on(self):
        """Return True if charger connected."""
        return self._car.charging_state != "Disconnected"

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "charging_state": self._car.charging_state,
            "conn_charge_cable": self._car.conn_charge_cable,
            "fast_charger_present": self._car.fast_charger_present,
            "fast_charger_brand": self._car.fast_charger_brand,
            "fast_charger_type": self._car.fast_charger_type,
        }


class TeslaCarCharging(TeslaCarEntity, BinarySensorEntity):
    """Representation of Tesla car charging binary sensor."""

    type = "charging"
    _attr_icon = "mdi:ev-station"
    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self._car.charging_state == "Charging"


class TeslaCarOnline(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car online binary sensor."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    type = "online"

    @property
    def is_on(self):
        """Return True if car is online."""
        return self._car.is_on

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "vehicle_id": str(self._car.vehicle_id),
            "vin": self._car.vin,
            "id": str(self._car.id),
            "state": self._car.state,
        }


class TeslaCarAsleep(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car asleep binary sensor."""

    type = "asleep"
    _attr_device_class = None
    _attr_icon = "mdi:sleep"

    @property
    def is_on(self):
        """Return True if car is asleep."""
        return self._car.state == "asleep"


class TeslaEnergyBatteryCharging(TeslaEnergyEntity, BinarySensorEntity):
    """Representation of a Tesla energy charging binary sensor."""

    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING
    _attr_icon = "mdi:battery-charging"
    type = "battery charging"

    @property
    def is_on(self) -> bool:
        """Return True if battery charging."""
        return self._energysite.battery_power < -100


class TeslaEnergyGridStatus(TeslaEnergyEntity, BinarySensorEntity):
    """Representation of the Tesla energy grid status binary sensor."""

    type = "grid status"
    _attr_device_class = BinarySensorDeviceClass.POWER

    @property
    def is_on(self) -> bool:
        """Return True if grid status is active."""
        return self._energysite.grid_status == GRID_ACTIVE


class TeslaCarDoors(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car door sensor."""

    type = "doors"
    _attr_device_class = BinarySensorDeviceClass.DOOR
    _attr_icon = "mdi:car-door"

    @property
    def is_on(self) -> bool:
        """Return True if a car door is open."""
        car = self._car
        return car.door_df or car.door_dr or car.door_pf or car.door_pr

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "Driver Front": self._open_or_closed(self._car.door_df),
            "Driver Rear": self._open_or_closed(self._car.door_dr),
            "Passenger Front": self._open_or_closed(self._car.door_pf),
            "Passenger Rear": self._open_or_closed(self._car.door_pr),
        }

    def _open_or_closed(self, door):
        """Return string of 'Open' or 'Closed' when passed a door integer state."""
        return "Open" if door else "Closed"


class TeslaCarWindows(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla window door sensor."""

    type = "windows"
    _attr_device_class = BinarySensorDeviceClass.WINDOW
    _attr_icon = "mdi:car-door"

    @property
    def is_on(self):
        """Return True if a car window is open."""
        car = self._car
        return car.window_fd or car.window_fp or car.window_rd or car.window_rp

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        car = self._car
        return {
            "Driver Front": self._open_or_closed(car.window_fd),
            "Driver Rear": self._open_or_closed(car.window_rd),
            "Passenger Front": self._open_or_closed(car.window_fp),
            "Passenger Rear": self._open_or_closed(car.window_rp),
        }

    def _open_or_closed(self, window):
        """Return string of 'Open' or 'Closed' when passed a window integer state."""
        if window:
            return "Open"
        return "Closed"


class TeslaCarScheduledCharging(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car scheduled charging binary sensor."""

    type = "scheduled charging"
    _attr_icon = "mdi:calendar-plus"
    _attr_device_class = None

    @property
    def is_on(self) -> bool:
        """Return True if scheduled charging enabled."""
        return self._car.scheduled_charging_mode == "StartAt"

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        # pylint: disable=protected-access
        timestamp = self._car._vehicle_data.get("charge_state", {}).get(
            "scheduled_charging_start_time"
        )
        return {
            "Scheduled charging time": self._car.scheduled_charging_start_time_app,
            "Scheduled charging timestamp": timestamp,
        }


class TeslaCarScheduledDeparture(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car scheduled departure binary sensor."""

    type = "scheduled departure"
    _attr_icon = "mdi:calendar-plus"
    _attr_device_class = None

    @property
    def is_on(self):
        """Return True if scheduled departure enebaled."""
        car = self._car
        return bool(
            car.scheduled_charging_mode == "DepartBy"
            or car.is_preconditioning_enabled
            or car.is_off_peak_charging_enabled
        )

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        # pylint: disable=protected-access
        car = self._car
        timestamp = car._vehicle_data.get("charge_state", {}).get(
            "scheduled_departure_time"
        )
        return {
            "Departure time": car.scheduled_departure_time_minutes,
            "Preconditioning enabled": car.is_preconditioning_enabled,
            "Preconditioning weekdays only": car.is_preconditioning_weekday_only,
            "Off peak charging enabled": car.is_off_peak_charging_enabled,
            "Off peak charging weekdays only": car.is_off_peak_charging_weekday_only,
            "End off peak time": car.off_peak_hours_end_time,
            "Departure timestamp": timestamp,
        }


class TeslaCarUserPresent(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car user present binary sensor."""

    type = "user present"
    _attr_icon = "mdi:account-check"
    _attr_device_class = None

    @property
    def is_on(self) -> bool:
        """Return True if user present enebaled."""
        # pylint: disable=protected-access
        return bool(
            self._car._vehicle_data.get("vehicle_state", {}).get("is_user_present")
        )

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        # pylint: disable=protected-access
        user_id = str(self._car._vehicle_data.get("user_id"))

        return {"user_id": user_id}
