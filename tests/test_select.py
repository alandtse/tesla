"""Tests for the Tesla select."""
from unittest.mock import patch

from homeassistant.components.select import DOMAIN as SELECT_DOMAIN
from homeassistant.const import ATTR_ENTITY_ID, SERVICE_SELECT_OPTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, SELECT_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("select.my_model_s_heated_seat_left")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_heated_seat_left"

    entry = entity_registry.async_get("select.my_model_s_heated_seat_right")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_heated_seat_right"

    entry = entity_registry.async_get("select.my_model_s_cabin_overheat_protection")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_cabin_overheat_protection"

    entry = entity_registry.async_get("select.battery_home_grid_charging")
    assert entry.unique_id == "67890_grid_charging"

    entry = entity_registry.async_get("select.battery_home_energy_exports")
    assert entry.unique_id == "67890_energy_exports"

    entry = entity_registry.async_get("select.battery_home_operation_mode")
    assert entry.unique_id == "67890_operation_mode"


async def test_car_heated_seat_select(hass: HomeAssistant) -> None:
    """Tests car heated seat select."""
    await setup_platform(hass, SELECT_DOMAIN)

    with patch(
        "teslajsonpy.car.TeslaCar.remote_seat_heater_request"
    ) as mock_remote_seat_heater_request:
        # Test selecting "Off"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {ATTR_ENTITY_ID: "select.my_model_s_heated_seat_left", "option": "Off"},
            blocking=True,
        )
        mock_remote_seat_heater_request.assert_awaited_once_with(0, 0)
        # Test selecting "Low"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {ATTR_ENTITY_ID: "select.my_model_s_heated_seat_left", "option": "Low"},
            blocking=True,
        )
        mock_remote_seat_heater_request.assert_awaited_with(1, 0)
        # Test selecting "Medium"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {ATTR_ENTITY_ID: "select.my_model_s_heated_seat_left", "option": "Medium"},
            blocking=True,
        )
        mock_remote_seat_heater_request.assert_awaited_with(2, 0)
        # Test selecting "High"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {ATTR_ENTITY_ID: "select.my_model_s_heated_seat_left", "option": "High"},
            blocking=True,
        )
        mock_remote_seat_heater_request.assert_awaited_with(3, 0)

    with patch(
        "teslajsonpy.car.TeslaCar.remote_auto_seat_climate_request"
    ) as mock_remote_auto_seat_climate_request:
        # Test selecting "Auto"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {ATTR_ENTITY_ID: "select.my_model_s_heated_seat_left", "option": "Auto"},
            blocking=True,
        )
        mock_remote_auto_seat_climate_request.assert_awaited_once_with(1, True)
        # Test from "Auto" selection
        car_mock_data.VEHICLE_DATA["climate_state"]["auto_seat_climate_left"] = True
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {ATTR_ENTITY_ID: "select.my_model_s_heated_seat_left", "option": "Low"},
            blocking=True,
        )
        mock_remote_auto_seat_climate_request.assert_awaited_with(1, False)

    with patch("teslajsonpy.car.TeslaCar.set_hvac_mode") as mock_set_hvac_mode:
        # Test climate_on check
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {ATTR_ENTITY_ID: "select.my_model_s_heated_seat_left", "option": "Low"},
            blocking=True,
        )
        mock_set_hvac_mode.assert_awaited_once_with("on")


async def test_cabin_overheat_protection(hass: HomeAssistant) -> None:
    """Tests car cabin overheat protection select."""
    await setup_platform(hass, SELECT_DOMAIN)

    with patch(
        "teslajsonpy.car.TeslaCar.set_cabin_overheat_protection"
    ) as mock_set_cabin_overheat_protection:
        # Test selecting "On"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {
                ATTR_ENTITY_ID: "select.my_model_s_cabin_overheat_protection",
                "option": "On",
            },
            blocking=True,
        )
        mock_set_cabin_overheat_protection.assert_awaited_once_with("On")
        # Test selecting "Off"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {
                ATTR_ENTITY_ID: "select.my_model_s_cabin_overheat_protection",
                "option": "Off",
            },
            blocking=True,
        )
        mock_set_cabin_overheat_protection.assert_awaited_with("Off")
        # Test selecting "No A/C"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {
                ATTR_ENTITY_ID: "select.my_model_s_cabin_overheat_protection",
                "option": "No A/C",
            },
            blocking=True,
        )
        mock_set_cabin_overheat_protection.assert_awaited_with("No A/C")


async def test_grid_charging(hass: HomeAssistant) -> None:
    """Tests energy site grid charging select."""
    await setup_platform(hass, SELECT_DOMAIN)

    with patch(
        "teslajsonpy.energy.SolarPowerwallSite.set_grid_charging"
    ) as mock_set_grid_charging:
        # Test selecting "Yes"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {
                ATTR_ENTITY_ID: "select.battery_home_grid_charging",
                "option": "Yes",
            },
            blocking=True,
        )
        mock_set_grid_charging.assert_awaited_once_with(True)
        # Test selecting "No"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {
                ATTR_ENTITY_ID: "select.battery_home_grid_charging",
                "option": "No",
            },
            blocking=True,
        )
        mock_set_grid_charging.assert_awaited_with(False)


async def test_energy_exports(hass: HomeAssistant) -> None:
    """Tests energy site energy exports select."""
    await setup_platform(hass, SELECT_DOMAIN)

    with patch(
        "teslajsonpy.energy.SolarPowerwallSite.set_export_rule"
    ) as mock_set_export_rule:
        # Test selecting "Solar"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {
                ATTR_ENTITY_ID: "select.battery_home_energy_exports",
                "option": "Solar",
            },
            blocking=True,
        )
        mock_set_export_rule.assert_awaited_once_with("pv_only")
        # Test selecting "Everything"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {
                ATTR_ENTITY_ID: "select.battery_home_energy_exports",
                "option": "Everything",
            },
            blocking=True,
        )
        mock_set_export_rule.assert_awaited_with("battery_ok")


async def test_operation_mode(hass: HomeAssistant) -> None:
    """Tests energy site operation mode select."""
    await setup_platform(hass, SELECT_DOMAIN)

    with patch(
        "teslajsonpy.energy.SolarPowerwallSite.set_operation_mode"
    ) as mock_set_operation_mode:
        # Test selecting "Self-Powered"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {
                ATTR_ENTITY_ID: "select.battery_home_operation_mode",
                "option": "Self-Powered",
            },
            blocking=True,
        )
        mock_set_operation_mode.assert_awaited_once_with("self_consumption")
        # Test selecting "Time-Based Control"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {
                ATTR_ENTITY_ID: "select.battery_home_operation_mode",
                "option": "Time-Based Control",
            },
            blocking=True,
        )
        mock_set_operation_mode.assert_awaited_with("autonomous")
        # Test selecting "Backup"
        assert await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {
                ATTR_ENTITY_ID: "select.battery_home_operation_mode",
                "option": "Backup",
            },
            blocking=True,
        )
        mock_set_operation_mode.assert_awaited_with("backup")
