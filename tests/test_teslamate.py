"""Tests for TeslaMate MQTT support."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from custom_components.tesla_custom.teslamate import MAP_VEHICLE_STATE, TeslaMate

from .mock_data import car as car_mock_data

pytestmark = pytest.mark.asyncio


async def test_get_car_from_id_skips_stale_vin_mapping() -> None:
    """Test stale VIN mappings do not block active TeslaMate car mappings."""
    active_car = SimpleNamespace(vin=car_mock_data.VIN)
    teslamate = object.__new__(TeslaMate)
    teslamate.cars = {car_mock_data.VIN: active_car}
    teslamate._data = {
        "car_map": {
            "stale-vin": "1",
            car_mock_data.VIN: "1",
        }
    }
    teslamate.async_load = AsyncMock()

    assert await teslamate.get_car_from_id("1") is active_car


async def test_center_display_state_mapping_updates_vehicle_state() -> None:
    """Test center_display_state MQTT topic maps into vehicle_state as an int."""
    # The topic is mapped to the vehicle_state sub-path.
    assert "center_display_state" in MAP_VEHICLE_STATE
    attr, cast = MAP_VEHICLE_STATE["center_display_state"]
    assert attr == "center_display_state"
    # TeslaMate publishes the value as a string payload; it must cast to int.
    assert cast("2") == 2

    car = SimpleNamespace(vin=car_mock_data.VIN, _vehicle_data={})
    TeslaMate.update_car_state(car, "vehicle_state", attr, cast("2"))

    assert car._vehicle_data["vehicle_state"]["center_display_state"] == 2
