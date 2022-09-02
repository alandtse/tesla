"""Tests for the Tesla climate."""

from homeassistant.components.climate import (
    DOMAIN as CLIMATE_DOMAIN,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, CLIMATE_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("climate.my_model_s_hvac_climate_system")
    assert entry.unique_id == "tesla_model_s_111111_hvac_climate_system"


# Test climate properties
