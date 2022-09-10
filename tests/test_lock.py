"""Tests for the Tesla lock."""
from unittest.mock import patch

from homeassistant.components.lock import DOMAIN as LOCK_DOMAIN
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_LOCK,
    SERVICE_UNLOCK,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, LOCK_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("lock.my_model_s_trunk")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_trunk"

    entry = entity_registry.async_get("lock.my_model_s_frunk")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_frunk"

    entry = entity_registry.async_get("lock.my_model_s_doors")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_doors"

    entry = entity_registry.async_get("lock.my_model_s_charger_door")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_charger_door"


async def test_car_trunk(hass: HomeAssistant) -> None:
    """Tests car trunk lock."""
    await setup_platform(hass, LOCK_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.toggle_trunk") as mock_toggle_trunk:
        assert await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_UNLOCK,
            {ATTR_ENTITY_ID: "lock.my_model_s_trunk"},
            blocking=True,
        )
        mock_toggle_trunk.assert_awaited_once()

    # Test SERVICE_UNLOCK but need to patch is_trunk_locked to return False


async def test_car_frunk(hass: HomeAssistant) -> None:
    """Tests car frunk lock."""
    await setup_platform(hass, LOCK_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.toggle_frunk") as mock_toggle_frunk:
        assert await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_UNLOCK,
            {ATTR_ENTITY_ID: "lock.my_model_s_frunk"},
            blocking=True,
        )
        mock_toggle_frunk.assert_awaited_once()

    # Test SERVICE_UNLOCK but need to patch is_frunk_locked to return False


async def test_car_door(hass: HomeAssistant) -> None:
    """Tests car door lock."""
    await setup_platform(hass, LOCK_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.unlock") as mock_unlock:
        assert await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_UNLOCK,
            {ATTR_ENTITY_ID: "lock.my_model_s_doors"},
            blocking=True,
        )
        mock_unlock.assert_awaited_once()

    with patch("teslajsonpy.car.TeslaCar.lock") as mock_unlock:
        assert await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_LOCK,
            {ATTR_ENTITY_ID: "lock.my_model_s_doors"},
            blocking=True,
        )
        mock_unlock.assert_awaited_once()


async def test_charger_door(hass: HomeAssistant) -> None:
    """Tests car charger door lock."""
    await setup_platform(hass, LOCK_DOMAIN)

    with patch(
        "teslajsonpy.car.TeslaCar.charge_port_door_open"
    ) as mock_charge_port_door_open:
        assert await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_UNLOCK,
            {ATTR_ENTITY_ID: "lock.my_model_s_charger_door"},
            blocking=True,
        )
        mock_charge_port_door_open.assert_awaited_once()

    with patch(
        "teslajsonpy.car.TeslaCar.charge_port_door_close"
    ) as mock_charge_port_door_close:
        assert await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_LOCK,
            {ATTR_ENTITY_ID: "lock.my_model_s_charger_door"},
            blocking=True,
        )
        mock_charge_port_door_close.assert_awaited_once()
