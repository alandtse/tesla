"""Tests for the Tesla button."""

from homeassistant.components.button import (
    DOMAIN as BUTTON_DOMAIN,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, BUTTON_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("button.my_model_s_horn")
    assert entry.unique_id == "tesla_model_s_111111_horn"

    entry = entity_registry.async_get("button.my_model_s_flash_lights")
    assert entry.unique_id == "tesla_model_s_111111_flash_lights"

    entry = entity_registry.async_get("button.my_model_s_wake_up")
    assert entry.unique_id == "tesla_model_s_111111_wake_up"

    entry = entity_registry.async_get("button.my_model_s_force_data_update")
    assert entry.unique_id == "tesla_model_s_111111_force_data_update"

    entry = entity_registry.async_get("button.my_model_s_trigger_homelink")
    assert entry.unique_id == "tesla_model_s_111111_trigger_homelink"


# Test button async_press
