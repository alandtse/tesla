"""Support for the Tesla sensors."""
from __future__ import annotations

from teslajsonpy.car import TeslaCar
from teslajsonpy.const import RESOURCE_TYPE_SOLAR, RESOURCE_TYPE_BATTERY
from teslajsonpy.energy import EnergySite, PowerwallSite

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    ENERGY_KILO_WATT_HOUR,
    ENERGY_WATT_HOUR,
    LENGTH_KILOMETERS,
    LENGTH_MILES,
    PERCENTAGE,
    TEMP_CELSIUS,
    POWER_WATT,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.icon import icon_for_battery_level
from homeassistant.util.distance import convert

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice, TeslaEnergyDevice
from .const import DOMAIN

SOLAR_SITE_SENSORS = ["solar_power", "grid_power", "load_power"]
BATTERY_SITE_SENSORS = SOLAR_SITE_SENSORS + ["battery_power"]


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla Sensors by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    energysites = hass.data[DOMAIN][config_entry.entry_id]["energysites"]
    entities = []

    for car in cars.values():
        entities.append(TeslaBattery(hass, car, coordinator))
        entities.append(TeslaChargerRate(hass, car, coordinator))
        entities.append(TeslaChargerEnergy(hass, car, coordinator))
        entities.append(TeslaMileage(hass, car, coordinator))
        entities.append(TeslaRange(hass, car, coordinator))
        entities.append(TeslaTemp(hass, car, coordinator))
        entities.append(TeslaTemp(hass, car, coordinator, inside=True))

    for energysite in energysites.values():
        if (
            energysite.resource_type == RESOURCE_TYPE_SOLAR
            and energysite.has_load_meter
        ):
            for sensor_type in SOLAR_SITE_SENSORS:
                entities.append(
                    TeslaEnergyPowerSensor(hass, energysite, coordinator, sensor_type)
                )
        elif energysite.resource_type == RESOURCE_TYPE_SOLAR:
            entities.append(
                TeslaEnergyPowerSensor(hass, energysite, coordinator, "solar_power")
            )

        if energysite.resource_type == RESOURCE_TYPE_BATTERY:
            entities.append(TeslaEnergyBattery(hass, energysite, coordinator))
            entities.append(TeslaEnergyBatteryRemaining(hass, energysite, coordinator))
            entities.append(TeslaEnergyBackupReserve(hass, energysite, coordinator))
            for sensor_type in BATTERY_SITE_SENSORS:
                entities.append(
                    TeslaEnergyPowerSensor(hass, energysite, coordinator, sensor_type)
                )

    async_add_entities(entities, True)


class TeslaBattery(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Car Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "battery"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_icon = "mdi:battery"

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return True

    @property
    def native_value(self) -> int:
        """Return the battery level."""
        return self._car.battery_level

    @property
    def icon(self):
        """Return the icon for the battery."""

        charging = self._car.battery_level == "Charging"

        return icon_for_battery_level(
            battery_level=self.native_value, charging=charging
        )


class TeslaChargerRate(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Car Charging Rate."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charging rate"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:speedometer"

    @property
    def native_unit_of_measurement(self) -> str:
        """Return Native Unit of Measurement.

        Get from Car setting
        """
        return self._car.gui_distance_units

    @property
    def native_value(self) -> int:
        """Return the battery Charge Rate."""
        charge_rate = self._car.charge_rate

        # If we don't have anything, just return None.
        if charge_rate is None:
            return charge_rate

        if self.unit_of_measurement == "km/hr":
            charge_rate = round(
                convert(charge_rate, LENGTH_MILES, LENGTH_KILOMETERS), 2
            )

        return charge_rate

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        added_range = self._car.charge_miles_added_ideal

        if self._car.gui_range_display == "Rated":
            added_range = self._car.charge_miles_added_rated

        if self.unit_of_measurement == "km/hr":
            added_range = round(
                convert(added_range, LENGTH_MILES, LENGTH_KILOMETERS), 2
            )

        data = {
            "time_left": self._car.time_to_full_charge,
            "added_range": added_range,
            "charge_energy_added": self._car.charge_energy_added,
            "charge_current_request": self._car.charge_current_request,
            "charge_current_request_max": self._car.charge_current_request_max,
            "charger_actual_current": self._car.charger_actual_current,
            "charger_voltage": self._car.charger_voltage,
            "charger_power": self._car.charger_power,
            "charger_phases": self._car.charger_phases,
            "charge_limit_soc": self._car.charge_limit_soc,
        }
        self.attrs.update(data)
        return self.attrs


class TeslaChargerEnergy(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Car Energy Added."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "energy added"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR
        self._attr_icon = "mdi:lightning-bolt"

    @property
    def native_value(self) -> int:
        """Return the Charge Energy Added."""
        return self._car.charge_energy_added


class TeslaMileage(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Car Mileage Added."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "mileage"
        self._attr_device_class = None
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_icon = "mdi:counter"

    @property
    def native_value(self) -> int:
        """Return the Charge Energy Added."""
        odometer_value = self._car.odometer

        if odometer_value is None:
            return None

        if self.native_unit_of_measurement == LENGTH_KILOMETERS:
            odometer_value = round(
                convert(odometer_value, LENGTH_MILES, LENGTH_KILOMETERS), 2
            )

        return round(odometer_value, 2)

    @property
    def native_unit_of_measurement(self) -> str:
        """Return Native Unit of Measurement.

        Get from Car setting
        """
        if self._car.gui_distance_units == "mi/hr":
            return LENGTH_MILES

        return LENGTH_KILOMETERS


class TeslaRange(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Car Range Added."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "range"
        self._attr_device_class = None
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:gauge"

    @property
    def native_value(self) -> int:
        """Return the Charge Energy Added."""
        range_value = self._car.battery_range

        if self._car.gui_range_display == "Ideal":
            range_value = self._car.ideal_battery_range

        if range_value is None:
            return None

        if self.native_unit_of_measurement == LENGTH_KILOMETERS:
            range_value = round(
                convert(range_value, LENGTH_MILES, LENGTH_KILOMETERS), 2
            )

        return range_value

    @property
    def native_unit_of_measurement(self) -> str:
        """Return Native Unit of Measurement.

        Get from Car setting
        """

        if self._car.gui_distance_units == "mi/hr":
            return LENGTH_MILES

        return LENGTH_KILOMETERS


class TeslaTemp(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Car Temp."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
        *,
        inside=False,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "temperature"
        self.inside = inside

        if inside is True:
            self.type += " (inside)"
        else:
            self.type += " (outside)"

        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:thermometer"

    @property
    def native_value(self) -> int:
        """Return the car temperature."""

        if self.inside is True:
            return self._car.inside_temp

        return self._car.outside_temp

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement.

        Tesla API always returns in Celsius.
        """
        return TEMP_CELSIUS


class TeslaEnergyPowerSensor(TeslaEnergyDevice, SensorEntity):
    """Representation of the Tesla Energy power sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: EnergySite,
        coordinator: TeslaDataUpdateCoordinator,
        sensor_type: str,
    ) -> None:
        """Initialize the Tesla energy power sensor."""
        super().__init__(hass, energysite, coordinator)
        self.type = sensor_type
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = POWER_WATT

        if self.type == "solar_power":
            self._attr_icon = "mdi:solar-power-variant"
            self._power = self._energysite.solar_power
        if self.type == "grid_power":
            self._attr_icon = "mdi:transmission-tower"
            self._power = self._energysite.grid_power
        if self.type == "load_power":
            self._attr_icon = "mdi:home-lightning-bolt"
            self._power = self._energysite.load_power
        if self.type == "battery_power":
            self._attr_icon = "mdi:home-battery"
            self._power = self._energysite.battery_power

    @property
    def native_value(self) -> int:
        """Return power in Watts."""
        return round(self._power)


class TeslaEnergyBattery(TeslaEnergyDevice, SensorEntity):
    """Representation of the Tesla Energy battery sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: PowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, energysite, coordinator)
        self.type = "battery"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = PERCENTAGE

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return True

    @property
    def native_value(self) -> int:
        """Return the battery level."""
        return round(self._energysite.percentage_charged)

    @property
    def icon(self):
        """Return the icon for the battery."""
        charging = self._energysite.battery_power < 0

        return icon_for_battery_level(
            battery_level=self.native_value, charging=charging
        )


class TeslaEnergyBatteryRemaining(TeslaEnergyDevice, SensorEntity):
    """Representation of the Tesla Energy battery remaining sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: PowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, energysite, coordinator)
        self.type = "battery remaining"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = ENERGY_WATT_HOUR

    @property
    def native_value(self) -> int:
        """Return the battery energy remaining."""
        return round(self._energysite.energy_left)

    @property
    def icon(self):
        """Return the icon for the battery remaining."""
        charging = self._energysite.battery_power < 0

        return icon_for_battery_level(
            battery_level=self._energysite.percentage_charged, charging=charging
        )


class TeslaEnergyBackupReserve(TeslaEnergyDevice, SensorEntity):
    """Representation of the Tesla Energy backup reserve sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: PowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, energysite, coordinator)
        self.type = "backup reserve"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self) -> int:
        """Return the backup reserve level."""
        return round(self._energysite.backup_reserve_percent)

    @property
    def icon(self):
        """Return the icon for the backup reserve."""
        return icon_for_battery_level(battery_level=self.native_value)
