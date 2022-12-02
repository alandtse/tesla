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
    LENGTH_MILES,
    PERCENTAGE,
    POWER_WATT,
    SPEED_KILOMETERS_PER_HOUR,
    SPEED_MILES_PER_HOUR,
    STATE_UNKNOWN,
    TEMP_CELSIUS,
    UnitOfPressure,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.util.unit_conversion import (
    DistanceConverter,
    SpeedConverter,
    PressureConverter,
)

from .common import setup_platform
from .mock_data import car as car_mock_data
from .mock_data import energysite as energysite_mock_data

from datetime import datetime, timedelta

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
        car_mock_data.VEHICLE_DATA["charge_state"]["usable_battery_level"]
    )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.BATTERY
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == PERCENTAGE
    assert (
        state.attributes.get("raw_soc")
        == car_mock_data.VEHICLE_DATA["charge_state"]["battery_level"]
    )


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

    if state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == SPEED_KILOMETERS_PER_HOUR:
        assert state.state == str(
            round(
                SpeedConverter.convert(
                    car_mock_data.VEHICLE_DATA["charge_state"]["charge_rate"],
                    SPEED_MILES_PER_HOUR,
                    SPEED_KILOMETERS_PER_HOUR,
                ),
                1,
            )
        )
    else:
        assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == SPEED_MILES_PER_HOUR
        assert state.state == str(
            car_mock_data.VEHICLE_DATA["charge_state"]["charge_rate"]
        )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.SPEED
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT

    assert (
        state.attributes.get("time_left")
        == car_mock_data.VEHICLE_DATA["charge_state"]["time_to_full_charge"]
    )


async def test_time_charge_complete_charging(hass: HomeAssistant) -> None:
    """Tests time charge complete is the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_time_charge_complete")
    charge_complete = datetime.utcnow() + timedelta(
        hours=float(car_mock_data.VEHICLE_DATA["charge_state"]["time_to_full_charge"])
    )
    charge_complete_str = datetime.strftime(charge_complete, "%Y-%m-%dT%H:%M:%S+00:00")

    assert state.state == charge_complete_str

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.TIMESTAMP
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT


async def test_time_charge_completed(hass: HomeAssistant) -> None:
    """Tests time charge complete is the correct value."""
    car_mock_data.VEHICLE_DATA["charge_state"]["time_to_full_charge"] = 0.0
    car_mock_data.VEHICLE_DATA["charge_state"]["charging_state"] = "Complete"
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_time_charge_complete")
    assert state.state == STATE_UNKNOWN


async def test_time_charge_stopped(hass: HomeAssistant) -> None:
    """Tests time charge complete is the correct value."""
    car_mock_data.VEHICLE_DATA["charge_state"]["time_to_full_charge"] = 0.0
    car_mock_data.VEHICLE_DATA["charge_state"]["charging_state"] = "Stopped"
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_model_s_time_charge_complete")
    assert state.state == STATE_UNKNOWN


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

    if state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == LENGTH_KILOMETERS:
        assert state.state == str(
            round(
                DistanceConverter.convert(
                    car_mock_data.VEHICLE_DATA["vehicle_state"]["odometer"],
                    LENGTH_MILES,
                    LENGTH_KILOMETERS,
                ),
                1,
            )
        )
    else:
        assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == LENGTH_MILES
        assert state.state == str(
            round(car_mock_data.VEHICLE_DATA["vehicle_state"]["odometer"], 1)
        )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.DISTANCE
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.TOTAL_INCREASING


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

    if state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == LENGTH_KILOMETERS:
        assert state.state == str(
            round(
                DistanceConverter.convert(
                    car_mock_data.VEHICLE_DATA["charge_state"]["battery_range"],
                    LENGTH_MILES,
                    LENGTH_KILOMETERS,
                ),
                2,
            )
        )
    else:
        assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == LENGTH_MILES
        assert state.state == str(
            car_mock_data.VEHICLE_DATA["charge_state"]["battery_range"]
        )

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.DISTANCE
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT


async def test_solar_power_value(hass: HomeAssistant) -> None:
    """Tests solar_power is getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state = hass.states.get("sensor.my_home_solar_power")
    assert state.state == str(round(energysite_mock_data.SITE_DATA["solar_power"]))

    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.POWER
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT


async def test_tpms_pressure_sensor(hass: HomeAssistant) -> None:
    """Tests tpms sensors are getting the correct value."""
    await setup_platform(hass, SENSOR_DOMAIN)

    state_fl = hass.states.get("sensor.my_model_s_tpms_front_left")
    assert state_fl.state == str(
        PressureConverter.convert(
            round(car_mock_data.VEHICLE_DATA["vehicle_state"]["tpms_pressure_fl"], 2),
            UnitOfPressure.BAR,
            UnitOfPressure.PSI,
        ),
    )

    assert state_fl.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.PRESSURE
    assert state_fl.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state_fl.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == UnitOfPressure.PSI

    assert (
        state_fl.attributes.get("tpms_last_seen_pressure_timestamp")
        == car_mock_data.VEHICLE_DATA["vehicle_state"][
            "tpms_last_seen_pressure_time_fl"
        ]
    )

    state_fr = hass.states.get("sensor.my_model_s_tpms_front_right")
    assert state_fr.state == str(
        PressureConverter.convert(
            round(car_mock_data.VEHICLE_DATA["vehicle_state"]["tpms_pressure_fr"], 2),
            UnitOfPressure.BAR,
            UnitOfPressure.PSI,
        ),
    )

    assert state_fr.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.PRESSURE
    assert state_fr.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state_fr.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == UnitOfPressure.PSI

    assert (
        state_fr.attributes.get("tpms_last_seen_pressure_timestamp")
        == car_mock_data.VEHICLE_DATA["vehicle_state"][
            "tpms_last_seen_pressure_time_fr"
        ]
    )

    state_rl = hass.states.get("sensor.my_model_s_tpms_rear_left")
    assert state_rl.state == str(
        PressureConverter.convert(
            round(car_mock_data.VEHICLE_DATA["vehicle_state"]["tpms_pressure_rl"], 2),
            UnitOfPressure.BAR,
            UnitOfPressure.PSI,
        ),
    )

    assert state_rl.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.PRESSURE
    assert state_rl.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state_rl.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == UnitOfPressure.PSI

    assert (
        state_rl.attributes.get("tpms_last_seen_pressure_timestamp")
        == car_mock_data.VEHICLE_DATA["vehicle_state"][
            "tpms_last_seen_pressure_time_rl"
        ]
    )

    state_rr = hass.states.get("sensor.my_model_s_tpms_rear_right")
    assert state_rr.state == str(
        PressureConverter.convert(
            round(car_mock_data.VEHICLE_DATA["vehicle_state"]["tpms_pressure_rr"], 2),
            UnitOfPressure.BAR,
            UnitOfPressure.PSI,
        ),
    )

    assert state_rr.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.PRESSURE
    assert state_rr.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state_rr.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == UnitOfPressure.PSI

    assert (
        state_rr.attributes.get("tpms_last_seen_pressure_timestamp")
        == car_mock_data.VEHICLE_DATA["vehicle_state"][
            "tpms_last_seen_pressure_time_rr"
        ]
    )
