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
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data

ATTR_STATE_CLASS = "state_class"


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests that the devices are registered in the entity registry."""
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("sensor.nikola_2_0_battery_sensor")
    assert entry.unique_id == "tesla_model_s_111111_battery_sensor"

    entry = entity_registry.async_get("sensor.nikola_2_0_charging_rate_sensor")
    assert entry.unique_id == "tesla_model_s_111111_charging_rate_sensor"

    entry = entity_registry.async_get("sensor.nikola_2_0_energy_added_sensor")
    assert entry.unique_id == "tesla_model_s_111111_energy_added_sensor"

    entry = entity_registry.async_get("sensor.nikola_2_0_mileage_sensor")
    assert entry.unique_id == "tesla_model_s_111111_mileage_sensor"

    entry = entity_registry.async_get("sensor.nikola_2_0_temperature_sensor_outside")
    assert entry.unique_id == "tesla_model_s_111111_temperature_sensor_outside"

    entry = entity_registry.async_get("sensor.nikola_2_0_temperature_sensor_inside")
    assert entry.unique_id == "tesla_model_s_111111_temperature_sensor_inside"


async def test_battery_value(hass: HomeAssistant) -> None:
    """Tests that the battery is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.nikola_2_0_battery_sensor")
    assert state.state == str(car_mock_data.CHARGE_STATE["battery_level"])

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.BATTERY
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == PERCENTAGE


async def test_charger_rate_value(hass: HomeAssistant) -> None:
    """Tests that the charger_rate is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.nikola_2_0_charging_rate_sensor")
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
    """Tests that the charger_energy is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.nikola_2_0_energy_added_sensor")
    assert state.state == str(car_mock_data.CHARGE_STATE["charge_energy_added"])

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.ENERGY
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.TOTAL_INCREASING
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == ENERGY_KILO_WATT_HOUR


async def test_mileage_value(hass: HomeAssistant) -> None:
    """Tests that the mileage is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.nikola_2_0_mileage_sensor")
    assert state.state == str(car_mock_data.VEHICLE_STATE["odometer"])

    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.TOTAL_INCREASING
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == LENGTH_MILES


async def test_range_value(hass: HomeAssistant) -> None:
    """Tests that the range is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.nikola_2_0_range_sensor")
    assert state.state == str(car_mock_data.CHARGE_STATE["ideal_battery_range"])

    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == LENGTH_MILES


async def test_inside_temp_value(hass: HomeAssistant) -> None:
    """Tests that the inside_temp is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.nikola_2_0_temperature_sensor_inside")
    assert state.state == str(car_mock_data.CLIMATE_STATE["inside_temp"])

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.TEMPERATURE
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == TEMP_CELSIUS


async def test_outside_temp_value(hass: HomeAssistant) -> None:
    """Tests that the outside_temp is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.nikola_2_0_temperature_sensor_outside")
    assert state.state == str(car_mock_data.CLIMATE_STATE["outside_temp"])

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.TEMPERATURE
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == TEMP_CELSIUS
