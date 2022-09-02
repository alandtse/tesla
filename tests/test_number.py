"""Tests for the Tesla number."""

from teslajsonpy.const import BACKUP_RESERVE_MAX, BACKUP_RESERVE_MIN, CHARGE_CURRENT_MIN

from homeassistant.components.number import DOMAIN as NUMBER_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data
from .mock_data import energysite as energysite_mock_data


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, NUMBER_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("number.my_model_s_charge_limit")
    assert entry.unique_id == "tesla_model_s_111111_charge_limit"

    entry = entity_registry.async_get("number.my_model_s_current_limit")
    assert entry.unique_id == "tesla_model_s_111111_current_limit"

    entry = entity_registry.async_get("number.battery_home_backup_reserve")
    assert entry.unique_id == "67890_backup_reserve"


async def test_charge_limit(hass: HomeAssistant) -> None:
    """Tests charge limit is getting the correct value."""
    await setup_platform(hass, NUMBER_DOMAIN)

    state = hass.states.get("number.my_model_s_charge_limit")
    assert state.state == str(car_mock_data.CHARGE_STATE["charge_limit_soc"])

    assert (
        state.attributes.get("min")
        == car_mock_data.CHARGE_STATE["charge_limit_soc_min"]
    )

    assert (
        state.attributes.get("max")
        == car_mock_data.CHARGE_STATE["charge_limit_soc_max"]
    )


# Need test for setting charge limit


async def test_current_limit(hass: HomeAssistant) -> None:
    """Tests current limit is getting the correct value."""
    await setup_platform(hass, NUMBER_DOMAIN)

    state = hass.states.get("number.my_model_s_current_limit")
    assert state.state == str(car_mock_data.CHARGE_STATE["charge_current_request"])

    assert state.attributes.get("min") == CHARGE_CURRENT_MIN

    assert (
        state.attributes.get("max")
        == car_mock_data.CHARGE_STATE["charge_current_request_max"]
    )


# Need test for setting current limit


async def test_backup_reserve(hass: HomeAssistant) -> None:
    """Tests backup reserve is getting the correct value."""
    await setup_platform(hass, NUMBER_DOMAIN)

    state = hass.states.get("number.battery_home_backup_reserve")
    assert state.state == str(
        energysite_mock_data.BATTERY_DATA["backup_reserve_percent"]
    )

    assert state.attributes.get("min") == BACKUP_RESERVE_MIN
    assert state.attributes.get("max") == BACKUP_RESERVE_MAX


# Need test for setting backup reserve
