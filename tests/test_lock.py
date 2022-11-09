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

    entry = entity_registry.async_get("lock.my_model_s_doors")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_doors"


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


async def test_charge_port_latch(hass: HomeAssistant) -> None:
    """Tests car charge port latch."""
    await setup_platform(hass, LOCK_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.charge_port_door_open") as mock_unlock:
        assert await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_UNLOCK,
            {ATTR_ENTITY_ID: "lock.my_model_s_charge_port_latch"},
            blocking=True,
        )
        mock_unlock.assert_awaited_once()
