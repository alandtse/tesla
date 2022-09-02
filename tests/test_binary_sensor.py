"""Tests for the Tesla binary sensor."""

from homeassistant.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from homeassistant.const import ATTR_DEVICE_CLASS
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, BINARY_SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("binary_sensor.my_model_s_parking_brake")
    assert entry.unique_id == "tesla_model_s_111111_parking_brake"

    entry = entity_registry.async_get("binary_sensor.my_model_s_charger")
    assert entry.unique_id == "tesla_model_s_111111_charger"

    entry = entity_registry.async_get("binary_sensor.my_model_s_charging")
    assert entry.unique_id == "tesla_model_s_111111_charging"

    entry = entity_registry.async_get("binary_sensor.my_model_s_online")
    assert entry.unique_id == "tesla_model_s_111111_online"

    entry = entity_registry.async_get("binary_sensor.battery_home_battery_charging")
    assert entry.unique_id == "67890_battery_charging"

    entry = entity_registry.async_get("binary_sensor.battery_home_grid_status")
    assert entry.unique_id == "67890_grid_status"


async def test_parking_brake(hass: HomeAssistant) -> None:
    """Tests parking brake is getting the correct value."""
    await setup_platform(hass, BINARY_SENSOR_DOMAIN)

    state = hass.states.get("binary_sensor.my_model_s_parking_brake")
    assert state.state == "off"

    assert state.attributes.get(ATTR_DEVICE_CLASS) is None


async def test_charger_connection(hass: HomeAssistant) -> None:
    """Tests charger connection is getting the correct value."""
    await setup_platform(hass, BINARY_SENSOR_DOMAIN)

    state = hass.states.get("binary_sensor.my_model_s_charger")
    assert state.state == "off"

    assert state.attributes.get(ATTR_DEVICE_CLASS) is None
    assert (
        state.attributes.get("charging_state")
        == car_mock_data.CHARGE_STATE["charging_state"]
    )
    assert (
        state.attributes.get("conn_charge_cable")
        == car_mock_data.CHARGE_STATE["conn_charge_cable"]
    )
    assert (
        state.attributes.get("fast_charger_present")
        == car_mock_data.CHARGE_STATE["fast_charger_present"]
    )
    assert (
        state.attributes.get("fast_charger_brand")
        == car_mock_data.CHARGE_STATE["fast_charger_brand"]
    )
    assert (
        state.attributes.get("fast_charger_type")
        == car_mock_data.CHARGE_STATE["fast_charger_type"]
    )


async def test_charging(hass: HomeAssistant) -> None:
    """Tests charging is getting the correct value."""
    await setup_platform(hass, BINARY_SENSOR_DOMAIN)

    state = hass.states.get("binary_sensor.my_model_s_charging")
    assert state.state == "off"

    assert (
        state.attributes.get(ATTR_DEVICE_CLASS)
        == BinarySensorDeviceClass.BATTERY_CHARGING
    )


# async def test_car_online(hass: HomeAssistant) -> None:
#     """Tests car online is getting the correct value."""
#     await setup_platform(hass, BINARY_SENSOR_DOMAIN)

#     state = hass.states.get("binary_sensor.my_model_s_online")
#     assert state.state == "on"

#     assert (
#         state.attributes.get(ATTR_DEVICE_CLASS) == BinarySensorDeviceClass.CONNECTIVITY
#     )
#     assert state.attributes.get("vehicle_id") == car_mock_data.VEHICLE["vehicle_id"]
#     assert state.attributes.get("vin") == car_mock_data.VEHICLE["vin"]
#     assert state.attributes.get("id") == car_mock_data.VEHICLE["id"]


async def test_battery_charging(hass: HomeAssistant) -> None:
    """Tests battery charging is getting the correct value."""
    await setup_platform(hass, BINARY_SENSOR_DOMAIN)

    state = hass.states.get("binary_sensor.battery_home_battery_charging")
    assert state.state == "on"

    assert (
        state.attributes.get(ATTR_DEVICE_CLASS)
        == BinarySensorDeviceClass.BATTERY_CHARGING
    )


async def test_grid_status(hass: HomeAssistant) -> None:
    """Tests grid status is getting the correct value."""
    await setup_platform(hass, BINARY_SENSOR_DOMAIN)

    state = hass.states.get("binary_sensor.battery_home_grid_status")
    assert state.state == "on"

    assert state.attributes.get(ATTR_DEVICE_CLASS) == BinarySensorDeviceClass.POWER
