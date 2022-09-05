"""Tests for the Tesla device tracker."""

from homeassistant.components.device_tracker import DOMAIN as DEVICE_TRACKER_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform

from .mock_data import car as car_mock_data


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, DEVICE_TRACKER_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("device_tracker.my_model_s_location_tracker")
    assert entry.unique_id == "tesla_model_s_111111_location_tracker"


async def test_car_location(hass: HomeAssistant) -> None:
    """Tests car location is getting the correct value."""
    await setup_platform(hass, DEVICE_TRACKER_DOMAIN)

    state = hass.states.get("device_tracker.my_model_s_location_tracker")

    assert state.attributes.get("heading") == car_mock_data.DRIVE_STATE["heading"]
    assert state.attributes.get("speed") == car_mock_data.DRIVE_STATE["speed"]
