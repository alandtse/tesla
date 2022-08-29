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
    LENGTH_MILES,
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
    assert entry.unique_id == "tesla_model_s_111111_battery"

    entry = entity_registry.async_get("sensor.my_model_s_charging_rate")
    assert entry.unique_id == "tesla_model_s_111111_charging_rate"

    entry = entity_registry.async_get("sensor.my_model_s_energy_added")
    assert entry.unique_id == "tesla_model_s_111111_energy_added"

    entry = entity_registry.async_get("sensor.my_model_s_mileage")
    assert entry.unique_id == "tesla_model_s_111111_mileage"

    entry = entity_registry.async_get("sensor.my_model_s_temperature_outside")
    assert entry.unique_id == "tesla_model_s_111111_temperature_outside"

    entry = entity_registry.async_get("sensor.my_model_s_temperature_inside")
    assert entry.unique_id == "tesla_model_s_111111_temperature_inside"

    entry = entity_registry.async_get("sensor.my_home_solar_power")
    assert entry.unique_id == "12345-solar_power"

    entry = entity_registry.async_get("sensor.my_home_grid_power")
    assert entry.unique_id == "12345-grid_power"

    entry = entity_registry.async_get("sensor.my_home_load_power")
    assert entry.unique_id == "12345-load_power"


async def test_battery_value(hass: HomeAssistant) -> None:
    """Tests battery is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_battery")
    assert state.state == str(car_mock_data.CHARGE_STATE["battery_level"])

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.BATTERY
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == PERCENTAGE


async def test_charger_rate_value(hass: HomeAssistant) -> None:
    """Tests charger_rate is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_charging_rate")
    assert state.state == str(car_mock_data.CHARGE_STATE["charge_rate"])

    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT

    assert (
        state.attributes.get("time_left")
        == car_mock_data.CHARGE_STATE["time_to_full_charge"]
    )
    assert (
        state.attributes.get("added_range")
        == car_mock_data.CHARGE_STATE["charge_miles_added_rated"]
    )
    assert (
        state.attributes.get("charge_energy_added")
        == car_mock_data.CHARGE_STATE["charge_energy_added"]
    )
    assert (
        state.attributes.get("charge_current_request")
        == car_mock_data.CHARGE_STATE["charge_current_request"]
    )
    assert (
        state.attributes.get("charge_current_request_max")
        == car_mock_data.CHARGE_STATE["charge_current_request_max"]
    )
    assert (
        state.attributes.get("charger_actual_current")
        == car_mock_data.CHARGE_STATE["charger_actual_current"]
    )
    assert (
        state.attributes.get("charger_voltage")
        == car_mock_data.CHARGE_STATE["charger_voltage"]
    )
    assert (
        state.attributes.get("charger_power")
        == car_mock_data.CHARGE_STATE["charger_power"]
    )
    assert (
        state.attributes.get("charger_phases")
        == car_mock_data.CHARGE_STATE["charger_phases"]
    )
    assert (
        state.attributes.get("charge_limit_soc")
        == car_mock_data.CHARGE_STATE["charge_limit_soc"]
    )


async def test_charger_energy_value(hass: HomeAssistant) -> None:
    """Tests charger_energy is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_energy_added")
    assert state.state == str(car_mock_data.CHARGE_STATE["charge_energy_added"])

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.ENERGY
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.TOTAL_INCREASING
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == ENERGY_KILO_WATT_HOUR


async def test_mileage_value(hass: HomeAssistant) -> None:
    """Tests mileage is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_mileage")
    assert state.state == str(car_mock_data.VEHICLE_STATE["odometer"])

    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.TOTAL_INCREASING
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == LENGTH_MILES


async def test_range_value(hass: HomeAssistant) -> None:
    """Tests range is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_range")
    assert state.state == str(car_mock_data.CHARGE_STATE["ideal_battery_range"])

    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == LENGTH_MILES


async def test_inside_temp_value(hass: HomeAssistant) -> None:
    """Tests inside_temp is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_temperature_inside")
    assert state.state == str(car_mock_data.CLIMATE_STATE["inside_temp"])

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.TEMPERATURE
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == TEMP_CELSIUS


async def test_outside_temp_value(hass: HomeAssistant) -> None:
    """Tests outside_temp is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_temperature_outside")
    assert state.state == str(car_mock_data.CLIMATE_STATE["outside_temp"])

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.TEMPERATURE
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == TEMP_CELSIUS


async def test_solar_power_value(hass: HomeAssistant) -> None:
    """Tests solar_power is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_home_solar_power")
    assert state.state == str(round(energysite_mock_data.SITE_DATA["solar_power"]))

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.POWER
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT


async def test_grid_power_value(hass: HomeAssistant) -> None:
    """Tests grid_power is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_home_grid_power")
    assert state.state == str(round(energysite_mock_data.SITE_DATA["grid_power"]))

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.POWER
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT


async def test_load_power_value(hass: HomeAssistant) -> None:
    """Tests load_power is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_home_load_power")
    assert state.state == str(round(energysite_mock_data.SITE_DATA["load_power"]))

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.POWER
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT
