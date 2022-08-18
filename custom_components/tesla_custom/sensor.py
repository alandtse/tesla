"""Support for the Tesla sensors."""
from __future__ import annotations

from teslajsonpy.const import TESLA_RESOURCE_TYPE_SOLAR, TESLA_RESOURCE_TYPE_BATTERY

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    ENERGY_KILO_WATT_HOUR,
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

    entities = []
    for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]:
        entities.append(TeslaBattery(hass, car, coordinator))
        entities.append(TeslaChargerRate(hass, car, coordinator))
        entities.append(TeslaChargerEnergy(hass, car, coordinator))
        entities.append(TeslaMileage(hass, car, coordinator))
        entities.append(TeslaRange(hass, car, coordinator))
        entities.append(TeslaTemp(hass, car, coordinator))
        entities.append(TeslaTemp(hass, car, coordinator, inside=True))

    for energysite in hass.data[DOMAIN][config_entry.entry_id]["energysites"]:
        if energysite["resource_type"] == TESLA_RESOURCE_TYPE_SOLAR:
            for sensor_type in SOLAR_SITE_SENSORS:
                entities.append(
                    TeslaEnergyPowerSensor(hass, energysite, coordinator, sensor_type)
                )

        if energysite["resource_type"] == TESLA_RESOURCE_TYPE_BATTERY:
            for sensor_type in BATTERY_SITE_SENSORS:
                entities.append(
                    TeslaEnergyPowerSensor(hass, energysite, coordinator, sensor_type)
                )

    async_add_entities(entities, True)


class TeslaBattery(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "battery sensor"
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
        return self.car.charging.get("battery_level")

    @property
    def icon(self):
        """Return the icon for the battery."""

        charging = self.car.charging.get("charging_state") == "Charging"

        return icon_for_battery_level(
            battery_level=self.native_value, charging=charging
        )


class TeslaChargerRate(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Charging Rate."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charging rate sensor"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:speedometer"

    @property
    def native_unit_of_measurement(self) -> str:
        """Return Native Unit of Measurement.

        Get from Car setting
        """
        return self.car.gui.get("gui_distance_units", "mi/hr")

    @property
    def native_value(self) -> int:
        """Return the battery Charge Rate."""
        charge_rate = self.car.charging.get("charge_rate")

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

        # we're going to be ref'ing this alot, so lets make a local var.

        c_data = self.car.charging

        added_range = c_data.get("charge_miles_added_ideal")

        if self.car.gui.get("gui_range_display") == "Rated":
            added_range = c_data.get("charge_miles_added_rated")

        if self.unit_of_measurement == "km/hr":
            added_range = round(
                convert(added_range, LENGTH_MILES, LENGTH_KILOMETERS), 2
            )

        data = {
            "time_left": c_data.get("time_to_full_charge"),
            "added_range": added_range,
            "charge_energy_added": c_data.get("charge_energy_added"),
            "charge_current_request": c_data.get("charge_current_request"),
            "charge_current_request_max": c_data.get("charge_current_request_max"),
            "charger_actual_current": c_data.get("charger_actual_current"),
            "charger_voltage": c_data.get("charger_voltage"),
            "charger_power": c_data.get("charger_power"),
            "charger_phases": c_data.get("charger_phases"),
            "charge_limit_soc": c_data.get("charge_limit_soc"),
        }
        self.attrs.update(data)
        return self.attrs


class TeslaChargerEnergy(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Energy Added."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "energy added sensor"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR
        self._attr_icon = "mdi:lightning-bolt"

    @property
    def native_value(self) -> int:
        """Return the Charge Energy Added."""
        charge_energy_added = self.car.charging.get("charge_energy_added")

        return charge_energy_added


class TeslaMileage(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Energy Added."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "mileage sensor"
        self._attr_device_class = None
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_icon = "mdi:counter"

    @property
    def native_value(self) -> int:
        """Return the Charge Energy Added."""
        odometer_value = self.car.state.get("odometer")

        if odometer_value is None:
            return None

        if self.native_unit_of_measurement == LENGTH_KILOMETERS:
            odometer_value = round(
                convert(odometer_value, LENGTH_MILES, LENGTH_KILOMETERS), 2
            )

        return odometer_value

    @property
    def native_unit_of_measurement(self) -> str:
        """Return Native Unit of Measurement.

        Get from Car setting
        """
        gui_uom = self.car.gui.get("gui_distance_units", "mi/hr")

        if gui_uom == "mi/hr":
            return LENGTH_MILES

        return LENGTH_KILOMETERS


class TeslaRange(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Energy Added."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "range sensor"
        self._attr_device_class = None
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:gauge"

    @property
    def native_value(self) -> int:
        """Return the Charge Energy Added."""
        range_value = self.car.charging.get("battery_range")

        if self.car.gui.get("gui_range_display") == "Rated":
            range_value = self.car.charging.get("ideal_battery_range")

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
        gui_uom = self.car.gui.get("gui_distance_units", "mi/hr")

        if gui_uom == "mi/hr":
            return LENGTH_MILES

        return LENGTH_KILOMETERS


class TeslaTemp(TeslaCarDevice, SensorEntity):
    """Representation of the Tesla Energy Added."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: dict,
        coordinator: TeslaDataUpdateCoordinator,
        *,
        inside=False,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "temperature sensor"
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
        """Return the Charge Energy Added."""

        if self.inside is True:
            return self.car.climate.get("inside_temp")

        return self.car.climate.get("outside_temp")

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement.

        Tesla API always returns in Celsius.
        """
        return TEMP_CELSIUS


class TeslaEnergyPowerSensor(TeslaEnergyDevice, SensorEntity):
    """Representation of the Tesla energy power sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: list,
        coordinator: TeslaDataUpdateCoordinator,
        sensor_type: str,
    ) -> None:
        """Initialize the Tesla energy power sensor."""
        super().__init__(hass, energysite, coordinator)
        self._name = sensor_type.replace("_", " ")
        self._sensor_type = sensor_type
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = POWER_WATT
        self._attr_unique_id = f"{self.energysite_id}-{self._sensor_type}"

    @property
    def native_value(self) -> int:
        """Return power in Watts."""

        return round(
            self.coordinator.controller.get_power(self.energysite_id, self._sensor_type)
        )
