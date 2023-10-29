"""Tests for the Tesla number."""
from unittest.mock import patch

from homeassistant.components.number import DOMAIN as NUMBER_DOMAIN
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from teslajsonpy.const import BACKUP_RESERVE_MAX, BACKUP_RESERVE_MIN, CHARGE_CURRENT_MIN

from .common import setup_platform
from .mock_data import car as car_mock_data, energysite as energysite_mock_data


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, NUMBER_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("number.my_model_s_charge_limit")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_charge_limit"

    entry = entity_registry.async_get("number.my_model_s_charging_amps")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_charging_amps"

    entry = entity_registry.async_get("number.battery_home_backup_reserve")
    assert entry.unique_id == "67890_backup_reserve"


async def test_charge_limit(hass: HomeAssistant) -> None:
    """Tests car charge limit is getting the correct value."""
    await setup_platform(hass, NUMBER_DOMAIN)

    state = hass.states.get("number.my_model_s_charge_limit")
    assert state.state == str(
        car_mock_data.VEHICLE_DATA["charge_state"]["charge_limit_soc"]
    )

    assert (
        state.attributes.get("min")
        == car_mock_data.VEHICLE_DATA["charge_state"]["charge_limit_soc_min"]
    )

    assert (
        state.attributes.get("max")
        == car_mock_data.VEHICLE_DATA["charge_state"]["charge_limit_soc_max"]
    )


async def test_set_charge_limit(hass: HomeAssistant) -> None:
    """Tests car set charge limit."""
    await setup_platform(hass, NUMBER_DOMAIN)

    with patch(
        "teslajsonpy.car.TeslaCar.change_charge_limit"
    ) as mock_change_charge_limit:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            "set_value",
            {ATTR_ENTITY_ID: "number.my_model_s_charge_limit", "value": 50.0},
            blocking=True,
        )
        mock_change_charge_limit.assert_awaited_once_with(50.0)


async def test_charging_amps(hass: HomeAssistant) -> None:
    """Tests car charging amps."""
    await setup_platform(hass, NUMBER_DOMAIN)

    state = hass.states.get("number.my_model_s_charging_amps")
    assert state.state == str(
        car_mock_data.VEHICLE_DATA["charge_state"]["charge_current_request"]
    )

    assert state.attributes.get("min") == CHARGE_CURRENT_MIN

    assert (
        state.attributes.get("max")
        == car_mock_data.VEHICLE_DATA["charge_state"]["charge_current_request_max"]
    )


async def test_set_charging_amps(hass: HomeAssistant) -> None:
    """Tests car set charging amps."""
    await setup_platform(hass, NUMBER_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.set_charging_amps") as mock_set_charging_amps:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            "set_value",
            {ATTR_ENTITY_ID: "number.my_model_s_charging_amps", "value": 15.0},
            blocking=True,
        )
        mock_set_charging_amps.assert_awaited_once_with(15.0)


async def test_backup_reserve(hass: HomeAssistant) -> None:
    """Tests energy site backup reserve is getting the correct value."""
    await setup_platform(hass, NUMBER_DOMAIN)

    state = hass.states.get("number.battery_home_backup_reserve")
    assert state.state == str(
        energysite_mock_data.BATTERY_DATA["backup"]["backup_reserve_percent"]
    )

    assert state.attributes.get("min") == BACKUP_RESERVE_MIN
    assert state.attributes.get("max") == BACKUP_RESERVE_MAX


async def test_set_backup_reserve(hass: HomeAssistant) -> None:
    """Tests energy site set backup reserve."""
    await setup_platform(hass, NUMBER_DOMAIN)

    with patch(
        "teslajsonpy.energy.PowerwallSite.set_reserve_percent"
    ) as mock_set_reserve_percent:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            "set_value",
            {ATTR_ENTITY_ID: "number.battery_home_backup_reserve", "value": 20.0},
            blocking=True,
        )
        mock_set_reserve_percent.assert_awaited_once_with(20.0)
