"""Tests for the Tesla sensor device."""

from homeassistant.components.sensor import (
    DOMAIN as SENSOR_DOMAIN,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_UNIT_OF_MEASUREMENT,
    ENERGY_KILO_WATT_HOUR,
    ENERGY_WATT_HOUR,
    LENGTH_KILOMETERS,
    PERCENTAGE,
    POWER_WATT,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data
from .mock_data import energysite as energysite_mock_data

ATTR_STATE_CLASS = "state_class"


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("sensor.my_model_s_battery")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_battery"

    entry = entity_registry.async_get("sensor.my_model_s_charging_rate")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_charging_rate"

    entry = entity_registry.async_get("sensor.my_model_s_energy_added")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_energy_added"

    entry = entity_registry.async_get("sensor.my_model_s_odometer")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_odometer"

    entry = entity_registry.async_get("sensor.my_model_s_temperature_outside")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_temperature_outside"

    entry = entity_registry.async_get("sensor.my_model_s_temperature_inside")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_temperature_inside"

    entry = entity_registry.async_get("sensor.my_home_solar_power")
    assert entry.unique_id == "12345_solar_power"

    entry = entity_registry.async_get("sensor.my_home_grid_power")
    assert entry.unique_id == "12345_grid_power"

    entry = entity_registry.async_get("sensor.my_home_load_power")
    assert entry.unique_id == "12345_load_power"

    entry = entity_registry.async_get("sensor.battery_home_battery_power")
    assert entry.unique_id == "67890_battery_power"

    entry = entity_registry.async_get("sensor.battery_home_battery")
    assert entry.unique_id == "67890_battery"

    entry = entity_registry.async_get("sensor.battery_home_battery_remaining")
    assert entry.unique_id == "67890_battery_remaining"

    entry = entity_registry.async_get("sensor.battery_home_backup_reserve")
    assert entry.unique_id == "67890_backup_reserve"


async def test_battery(hass: HomeAssistant) -> None:
    """Tests battery is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.battery_home_battery")
    assert state.state == str(
        round(energysite_mock_data.BATTERY_SUMMARY["percentage_charged"])
    )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.BATTERY
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == PERCENTAGE


async def test_battery_power_value(hass: HomeAssistant) -> None:
    """Tests battery_power is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.battery_home_battery_power")
    assert state.state == str(
        round(energysite_mock_data.BATTERY_DATA["power_reading"][0]["battery_power"])
    )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.POWER
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT


async def test_battery_remaining(hass: HomeAssistant) -> None:
    """Tests battery remaining is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.battery_home_battery_remaining")
    assert state.state == str(
        round(energysite_mock_data.BATTERY_SUMMARY["energy_left"])
    )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.BATTERY
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == ENERGY_WATT_HOUR


async def test_backup_reserve(hass: HomeAssistant) -> None:
    """Tests backup reserve is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.battery_home_backup_reserve")
    assert state.state == str(
        round(energysite_mock_data.BATTERY_DATA["backup"]["backup_reserve_percent"])
    )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.BATTERY
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == PERCENTAGE


async def test_battery_value(hass: HomeAssistant) -> None:
    """Tests battery is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_battery")
    assert state.state == str(
        car_mock_data.VEHICLE_DATA["charge_state"]["battery_level"]
    )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.BATTERY
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == PERCENTAGE


async def test_charger_energy_value(hass: HomeAssistant) -> None:
    """Tests charger_energy is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_energy_added")
    assert state.state == str(
        car_mock_data.VEHICLE_DATA["charge_state"]["charge_energy_added"]
    )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.ENERGY
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.TOTAL_INCREASING
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == ENERGY_KILO_WATT_HOUR


async def test_charger_power_value(hass: HomeAssistant) -> None:
    """Tests charger_power is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_charger_power")
    assert state.state == str(
        car_mock_data.VEHICLE_DATA["charge_state"]["charger_power"]
    )

    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT

    assert (
        state.attributes.get("charger_amps_request")
        == car_mock_data.VEHICLE_DATA["charge_state"]["charge_current_request"]
    )
    assert (
        state.attributes.get("charger_amps_actual")
        == car_mock_data.VEHICLE_DATA["charge_state"]["charger_actual_current"]
    )
    assert (
        state.attributes.get("charger_volts")
        == car_mock_data.VEHICLE_DATA["charge_state"]["charger_voltage"]
    )
    assert (
        state.attributes.get("charger_phases")
        == car_mock_data.VEHICLE_DATA["charge_state"]["charger_phases"]
    )


async def test_charger_rate_value(hass: HomeAssistant) -> None:
    """Tests charger_rate is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_charging_rate")
    # Test state against km/hr
    # Tesla API returns in miles so manually set charge rate to km/hr
    assert state.state == "37.34"

    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT

    assert (
        state.attributes.get("time_left")
        == car_mock_data.VEHICLE_DATA["charge_state"]["time_to_full_charge"]
    )


async def test_grid_power_value(hass: HomeAssistant) -> None:
    """Tests grid_power is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_home_grid_power")
    assert state.state == str(round(energysite_mock_data.SITE_DATA["grid_power"]))

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.POWER
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT


async def test_inside_temp_value(hass: HomeAssistant) -> None:
    """Tests inside_temp is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_temperature_inside")
    assert state.state == str(
        car_mock_data.VEHICLE_DATA["climate_state"]["inside_temp"]
    )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.TEMPERATURE
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == TEMP_CELSIUS


async def test_load_power_value(hass: HomeAssistant) -> None:
    """Tests load_power is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_home_load_power")
    assert state.state == str(round(energysite_mock_data.SITE_DATA["load_power"]))

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.POWER
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT


async def test_odometer_value(hass: HomeAssistant) -> None:
    """Tests odometer is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_odometer")
    # Test state against odometer in kilometers
    # Tesla API returns in miles so manually set range in kilometers
    assert state.state == "114127.59"

    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.TOTAL_INCREASING
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == LENGTH_KILOMETERS


async def test_outside_temp_value(hass: HomeAssistant) -> None:
    """Tests outside_temp is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_temperature_outside")
    assert state.state == str(
        car_mock_data.VEHICLE_DATA["climate_state"]["outside_temp"]
    )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.TEMPERATURE
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == TEMP_CELSIUS


async def test_range_value(hass: HomeAssistant) -> None:
    """Tests range is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_range")
    # Test state against range in kilometers
    # Tesla API returns in miles so manually set range in kilometers
    assert state.state == "272.11"

    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == LENGTH_KILOMETERS


async def test_solar_power_value(hass: HomeAssistant) -> None:
    """Tests solar_power is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_home_solar_power")
    assert state.state == str(round(energysite_mock_data.SITE_DATA["solar_power"]))

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.POWER
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT
