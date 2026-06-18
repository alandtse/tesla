"""Tests for the Tesla lock."""

from unittest.mock import AsyncMock, patch

from homeassistant.components.lock import DOMAIN as LOCK_DOMAIN
from homeassistant.const import ATTR_ENTITY_ID, SERVICE_LOCK, SERVICE_UNLOCK
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
import pytest

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
        await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_UNLOCK,
            {ATTR_ENTITY_ID: "lock.my_model_s_doors"},
            blocking=True,
        )
        mock_unlock.assert_awaited_once()

    with patch("teslajsonpy.car.TeslaCar.lock") as mock_unlock:
        await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_LOCK,
            {ATTR_ENTITY_ID: "lock.my_model_s_doors"},
            blocking=True,
        )
        mock_unlock.assert_awaited_once()


@pytest.mark.parametrize("vehicle_state", [None, pytest.param({}, id="missing")])
async def test_car_door_unlock_without_vehicle_state(
    hass: HomeAssistant, vehicle_state: dict | None
) -> None:
    """Tests car door unlock handles unavailable vehicle state."""
    _, mock_controller = await setup_platform(hass, LOCK_DOMAIN)
    car = mock_controller.return_value.generate_car_objects.return_value[
        car_mock_data.VIN
    ]
    original_vehicle_state = car._vehicle_data.get("vehicle_state")

    try:
        if vehicle_state is None:
            car._vehicle_data["vehicle_state"] = None
        else:
            car._vehicle_data.pop("vehicle_state")
        car._send_command = AsyncMock(
            return_value={"response": {"result": True, "reason": ""}}
        )

        await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_UNLOCK,
            {ATTR_ENTITY_ID: "lock.my_model_s_doors"},
            blocking=True,
        )

        car._send_command.assert_awaited_once_with("UNLOCK")
        assert car._vehicle_data["vehicle_state"]["locked"] is False
    finally:
        car._vehicle_data["vehicle_state"] = original_vehicle_state


async def test_charge_port_latch(hass: HomeAssistant) -> None:
    """Tests car charge port latch."""
    await setup_platform(hass, LOCK_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.charge_port_door_open") as mock_unlock:
        await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_UNLOCK,
            {ATTR_ENTITY_ID: "lock.my_model_s_charge_port_latch"},
            blocking=True,
        )
        mock_unlock.assert_awaited_once()
