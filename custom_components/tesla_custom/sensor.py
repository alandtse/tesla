"""Support for the Tesla sensors."""

from datetime import datetime, timedelta
from typing import Optional

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfLength,
    UnitOfPower,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.icon import icon_for_battery_level
from homeassistant.util import dt
from homeassistant.util.unit_conversion import DistanceConverter
from teslajsonpy.car import TeslaCar
from teslajsonpy.const import RESOURCE_TYPE_BATTERY, RESOURCE_TYPE_SOLAR
from teslajsonpy.energy import EnergySite

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity, TeslaEnergyEntity
from .const import DISTANCE_UNITS_KM_HR, DOMAIN

SOLAR_SITE_SENSORS = ["solar power", "grid power", "load power"]
BATTERY_SITE_SENSORS = SOLAR_SITE_SENSORS + ["battery power"]

TPMS_SENSORS = {
    "TPMS front left": "tpms_pressure_fl",
    "TPMS front right": "tpms_pressure_fr",
    "TPMS rear left": "tpms_pressure_rl",
    "TPMS rear right": "tpms_pressure_rr",
}

TPMS_SENSOR_ATTR = {
    "TPMS front left": "tpms_last_seen_pressure_time_fl",
    "TPMS front right": "tpms_last_seen_pressure_time_fr",
    "TPMS rear left": "tpms_last_seen_pressure_time_rl",
    "TPMS rear right": "tpms_last_seen_pressure_time_rr",
}


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla Sensors by config_entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinators = entry_data["coordinators"]
    cars = entry_data["cars"]
    energysites = entry_data["energysites"]
    entities = []

    for vin, car in cars.items():
        coordinator = coordinators[vin]
        entities.append(TeslaCarBattery(car, coordinator))
        entities.append(TeslaCarChargerRate(car, coordinator))
        entities.append(TeslaCarChargerEnergy(car, coordinator))
        entities.append(TeslaCarChargerPower(car, coordinator))
        entities.append(TeslaCarOdometer(car, coordinator))
        entities.append(TeslaCarShiftState(car, coordinator))
        entities.append(TeslaCarRange(car, coordinator))
        entities.append(TeslaCarTemp(car, coordinator))
        entities.append(TeslaCarTemp(car, coordinator, inside=True))
        entities.append(TeslaCarTimeChargeComplete(car, coordinator))
        for tpms_sensor in TPMS_SENSORS:
            entities.append(TeslaCarTpmsPressureSensor(car, coordinator, tpms_sensor))
        entities.append(TeslaCarArrivalTime(car, coordinator))
        entities.append(TeslaCarDistanceToArrival(car, coordinator))
        entities.append(TeslaCarDataUpdateTime(car, coordinator))
        entities.append(TeslaCarPollingInterval(car, coordinator))

    for energy_site_id, energysite in energysites.items():
        coordinator = coordinators[energy_site_id]
        if (
            energysite.resource_type == RESOURCE_TYPE_SOLAR
            and energysite.has_load_meter
        ):
            for sensor_type in SOLAR_SITE_SENSORS:
                entities.append(
                    TeslaEnergyPowerSensor(energysite, coordinator, sensor_type)
                )
        elif energysite.resource_type == RESOURCE_TYPE_SOLAR:
            entities.append(
                TeslaEnergyPowerSensor(energysite, coordinator, "solar power")
            )

        if energysite.resource_type == RESOURCE_TYPE_BATTERY:
            entities.append(TeslaEnergyBattery(energysite, coordinator))
            entities.append(TeslaEnergyBatteryRemaining(energysite, coordinator))
            entities.append(TeslaEnergyBackupReserve(energysite, coordinator))
            for sensor_type in BATTERY_SITE_SENSORS:
                entities.append(
                    TeslaEnergyPowerSensor(energysite, coordinator, sensor_type)
                )

    async_add_entities(entities, update_before_add=True)


class TeslaCarBattery(TeslaCarEntity, SensorEntity):
    """Representation of the Tesla car battery sensor."""

    type = "battery"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:battery"

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return True

    @property
    def native_value(self) -> int:
        """Return battery level."""
        # usable_battery_level matches the Tesla app and car display
        return self._car.usable_battery_level

    @property
    def icon(self):
        """Return icon for the battery."""
        charging = self._car.charging_state == "Charging"

        return icon_for_battery_level(
            battery_level=self.native_value, charging=charging
        )

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "raw_soc": self._car.battery_level,
        }


class TeslaCarChargerEnergy(TeslaCarEntity, SensorEntity):
    """Representation of a Tesla car energy added sensor."""

    type = "energy added"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_icon = "mdi:lightning-bolt"

    @property
    def native_value(self) -> float:
        """Return the charge energy added."""
        # The car will reset this to 0 automatically when charger
        # goes from disconnected to connected
        return self._car.charge_energy_added

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        if self._car.charge_miles_added_rated:
            added_range = self._car.charge_miles_added_rated
        elif (
            self._car.charge_miles_added_ideal
            and self._car.gui_range_display == "Ideal"
        ):
            added_range = self._car.charge_miles_added_ideal
        else:
            added_range = 0

        if self._car.gui_distance_units == DISTANCE_UNITS_KM_HR:
            added_range = DistanceConverter.convert(
                added_range, UnitOfLength.MILES, UnitOfLength.KILOMETERS
            )

        return {
            "added_range": round(added_range, 2),
        }


class TeslaCarChargerPower(TeslaCarEntity, SensorEntity):
    """Representation of a Tesla car charger power."""

    type = "charger power"
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT

    @property
    def native_value(self) -> float:
        """Return the charger power."""
        return (
            float(self._car.charger_power)
            if self._car.charger_power is not None
            else self._car.charger_power
        )

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        car = self._car
        return {
            "charger_amps_request": car.charge_current_request,
            "charger_amps_actual": car.charger_actual_current,
            "charger_volts": car.charger_voltage,
            "charger_phases": car.charger_phases,
        }


class TeslaCarChargerRate(TeslaCarEntity, SensorEntity):
    """Representation of the Tesla car charging rate."""

    type = "charging rate"
    _attr_device_class = SensorDeviceClass.SPEED
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfSpeed.MILES_PER_HOUR
    _attr_icon = "mdi:speedometer"

    @property
    def native_value(self) -> float:
        """Return charge rate."""
        charge_rate = self._car.charge_rate

        if charge_rate is None:
            return charge_rate

        return round(charge_rate, 2)

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "time_left": self._car.time_to_full_charge,
        }


class TeslaCarOdometer(TeslaCarEntity, SensorEntity):
    """Representation of the Tesla car odometer sensor."""

    type = "odometer"
    _attr_device_class = SensorDeviceClass.DISTANCE
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfLength.MILES
    _attr_icon = "mdi:counter"

    @property
    def native_value(self) -> float:
        """Return the odometer."""
        odometer_value = self._car.odometer

        if odometer_value is None:
            return None

        return round(odometer_value, 2)


class TeslaCarShiftState(TeslaCarEntity, SensorEntity):
    """Representation of the Tesla car Shift State sensor."""

    type = "shift state"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_icon = "mdi:car-shift-pattern"

    @property
    def native_value(self) -> float:
        """Return the shift state."""
        value = self._car.shift_state

        # When car is parked and off, Tesla API reports shift_state None
        if value is None or value == "":
            return "P"

        return value

    @property
    def options(self) -> float:
        """Return the values for the ENUM."""
        values = ["P", "D", "R", "N"]

        return values

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""

        return {
            "raw_state": self._car.shift_state,
        }


class TeslaCarRange(TeslaCarEntity, SensorEntity):
    """Representation of the Tesla car range sensor."""

    type = "range"
    _attr_device_class = SensorDeviceClass.DISTANCE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfLength.MILES
    _attr_icon = "mdi:gauge"

    @property
    def native_value(self) -> float:
        """Return range."""
        car = self._car
        range_value = car.battery_range

        if car.gui_range_display == "Ideal":
            range_value = car.ideal_battery_range

        if range_value is None:
            return None

        return round(range_value, 2)

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        # pylint: disable=protected-access
        est_battery_range = self._car._vehicle_data.get("charge_state", {}).get(
            "est_battery_range"
        )
        if est_battery_range is not None:
            est_battery_range_km = DistanceConverter.convert(
                est_battery_range, UnitOfLength.MILES, UnitOfLength.KILOMETERS
            )
        else:
            est_battery_range_km = None

        return {
            "est_battery_range_miles": est_battery_range,
            "est_battery_range_km": est_battery_range_km,
        }


class TeslaCarTemp(TeslaCarEntity, SensorEntity):
    """Representation of a Tesla car temp sensor."""

    type = "temperature"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_icon = "mdi:thermometer"

    def __init__(
        self,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
        *,
        inside=False,
    ) -> None:
        """Initialize temp entity."""
        self.inside = inside
        if inside is True:
            self.type += " (inside)"
        else:
            self.type += " (outside)"
        super().__init__(car, coordinator)

    @property
    def native_value(self) -> float:
        """Return car temperature."""
        if self.inside is True:
            return self._car.inside_temp
        return self._car.outside_temp


class TeslaEnergyPowerSensor(TeslaEnergyEntity, SensorEntity):
    """Representation of a Tesla energy power sensor."""

    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.WATT

    def __init__(
        self,
        energysite: EnergySite,
        coordinator: TeslaDataUpdateCoordinator,
        sensor_type: str,
    ) -> None:
        """Initialize power sensor."""
        self.type = sensor_type
        if self.type == "solar power":
            self._attr_icon = "mdi:solar-power-variant"
        if self.type == "grid power":
            self._attr_icon = "mdi:transmission-tower"
        if self.type == "load power":
            self._attr_icon = "mdi:home-lightning-bolt"
        if self.type == "battery power":
            self._attr_icon = "mdi:home-battery"
        super().__init__(energysite, coordinator)

    @property
    def native_value(self) -> float:
        """Return power in Watts."""
        if self.type == "solar power":
            return round(self._energysite.solar_power)
        if self.type == "grid power":
            return round(self._energysite.grid_power)
        if self.type == "load power":
            return round(self._energysite.load_power)
        if self.type == "battery power":
            return round(self._energysite.battery_power)
        return 0


class TeslaEnergyBattery(TeslaEnergyEntity, SensorEntity):
    """Representation of the Tesla energy battery sensor."""

    type = "battery"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return True

    @property
    def native_value(self) -> int:
        """Return battery level."""
        return round(self._energysite.percentage_charged)

    @property
    def icon(self):
        """Return icon for the battery."""
        charging = self._energysite.battery_power < -100

        return icon_for_battery_level(
            battery_level=self.native_value, charging=charging
        )


class TeslaEnergyBatteryRemaining(TeslaEnergyEntity, SensorEntity):
    """Representation of a Tesla energy battery remaining sensor."""

    type = "battery remaining"
    _attr_device_class = SensorDeviceClass.ENERGY_STORAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR

    @property
    def native_value(self) -> int:
        """Return battery energy remaining."""
        return round(self._energysite.energy_left)

    @property
    def icon(self):
        """Return icon for the battery remaining."""
        charging = self._energysite.battery_power < -100

        return icon_for_battery_level(
            battery_level=self._energysite.percentage_charged, charging=charging
        )


class TeslaEnergyBackupReserve(TeslaEnergyEntity, SensorEntity):
    """Representation of a Tesla energy backup reserve sensor."""

    type = "backup reserve"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self) -> int:
        """Return backup reserve level."""
        return round(self._energysite.backup_reserve_percent)

    @property
    def icon(self):
        """Return icon for the backup reserve."""
        return icon_for_battery_level(battery_level=self.native_value)


class TeslaCarTimeChargeComplete(TeslaCarEntity, SensorEntity):
    """Representation of the Tesla car time charge complete."""

    type = "time charge complete"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:timer-plus"
    _value: Optional[datetime] = None
    _last_known_value: Optional[int] = None
    _last_update_time: Optional[datetime] = None

    @property
    def native_value(self) -> Optional[datetime]:
        """Return time charge complete."""
        if self._car.time_to_full_charge is None:
            charge_hours = 0
        else:
            charge_hours = float(self._car.time_to_full_charge)

        if self._last_known_value != charge_hours:
            self._last_known_value = charge_hours
            self._last_update_time = dt.utcnow()

        if self._car.charging_state == "Charging" and charge_hours > 0:
            new_value = (
                dt.utcnow()
                + timedelta(hours=charge_hours)
                - (dt.utcnow() - self._last_update_time)
            )
            if (
                self._value is None
                or abs((new_value - self._value).total_seconds()) >= 60
            ):
                self._value = new_value
        if self._car.charging_state in ["Charging", "Complete"]:
            return self._value
        return None

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        # pylint: disable=protected-access
        minutes_to_full_charge = self._car._vehicle_data.get("charge_state", {}).get(
            "minutes_to_full_charge"
        )

        return {
            "minutes_to_full_charge": minutes_to_full_charge,
        }


class TeslaCarTpmsPressureSensor(TeslaCarEntity, SensorEntity):
    """Representation of the Tesla car TPMS Pressure sensor."""

    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPressure.BAR
    _attr_suggested_unit_of_measurement = UnitOfPressure.PSI
    _attr_icon = "mdi:gauge-full"

    def __init__(
        self,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
        tpms_sensor: str,
    ) -> None:
        """Initialize TPMS Pressure sensor."""
        self._tpms_sensor = tpms_sensor
        self.type = tpms_sensor
        super().__init__(car, coordinator)

    @property
    def native_value(self) -> float:
        """Return TPMS Pressure."""
        value = getattr(self._car, TPMS_SENSORS.get(self._tpms_sensor))
        if value is not None:
            value = round(value, 2)
        return value

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        # pylint: disable=protected-access
        timestamp = self._car._vehicle_data.get("vehicle_state", {}).get(
            TPMS_SENSOR_ATTR.get(self._tpms_sensor)
        )

        return {
            "tpms_last_seen_pressure_timestamp": timestamp,
        }


class TeslaCarArrivalTime(TeslaCarEntity, SensorEntity):
    """Representation of the Tesla car route arrival time."""

    type = "arrival time"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:timer-sand"
    _datetime_value: Optional[datetime] = None
    _last_known_value: Optional[int] = None
    _last_update_time: Optional[datetime] = None

    @property
    def native_value(self) -> Optional[datetime]:
        """Return route arrival time."""
        if self._car.active_route_minutes_to_arrival is None:
            return self._datetime_value
        min_duration = round(float(self._car.active_route_minutes_to_arrival), 2)

        utcnow = dt.utcnow()
        if self._last_known_value != min_duration:
            self._last_known_value = min_duration
            self._last_update_time = utcnow

        new_value = (
            utcnow + timedelta(minutes=min_duration) - (utcnow - self._last_update_time)
        )
        if (
            self._datetime_value is None
            or abs((new_value - self._datetime_value).total_seconds()) >= 60
        ):
            self._datetime_value = new_value
        return self._datetime_value

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        car = self._car
        if car.active_route_traffic_minutes_delay is None:
            minutes = None
        else:
            minutes = round(car.active_route_traffic_minutes_delay, 1)

        return {
            "Energy at arrival": car.active_route_energy_at_arrival,
            "Minutes traffic delay": minutes,
            "Destination": car.active_route_destination,
            "Minutes to arrival": (
                None
                if car.active_route_minutes_to_arrival is None
                else round(float(car.active_route_minutes_to_arrival), 2)
            ),
        }


class TeslaCarDistanceToArrival(TeslaCarEntity, SensorEntity):
    """Representation of the Tesla distance to arrival."""

    type = "distance to arrival"
    _attr_device_class = SensorDeviceClass.DISTANCE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfLength.MILES
    _attr_icon = "mdi:map-marker-distance"

    @property
    def native_value(self) -> float:
        """Return the distance to arrival."""
        if self._car.active_route_miles_to_arrival is None:
            return None
        return round(self._car.active_route_miles_to_arrival, 2)


class TeslaCarDataUpdateTime(TeslaCarEntity, SensorEntity):
    """Representation of the TeslajsonPy Last Data Update time."""

    type = "data last update time"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:timer"

    @property
    def native_value(self) -> datetime:
        """Return the last data update time."""
        last_time = self.coordinator.controller.get_last_update_time(vin=self._car.vin)
        if not isinstance(last_time, datetime):
            date_obj = datetime.fromtimestamp(last_time, dt.UTC)
        else:
            date_obj = last_time.replace(tzinfo=dt.UTC)
        return date_obj


class TeslaCarPollingInterval(TeslaCarEntity, SensorEntity):
    """Representation of a Tesla car polling interval."""

    type = "polling interval"
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:timer-sync"

    @property
    def native_value(self) -> int:
        """Return the update time interval."""
        return self.coordinator.controller.get_update_interval_vin(vin=self._car.vin)
