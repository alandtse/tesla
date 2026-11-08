"""Tests for TeslaMate MQTT support."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from custom_components.tesla_custom.teslamate import TeslaMate

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
