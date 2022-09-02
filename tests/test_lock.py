"""Tests for the Tesla lock."""

from homeassistant.components.lock import DOMAIN as LOCK_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, LOCK_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("lock.my_model_s_trunk_lock")
    assert entry.unique_id == "tesla_model_s_111111_trunk_lock"

    entry = entity_registry.async_get("lock.my_model_s_frunk_lock")
    assert entry.unique_id == "tesla_model_s_111111_frunk_lock"

    entry = entity_registry.async_get("lock.my_model_s_door_lock")
    assert entry.unique_id == "tesla_model_s_111111_door_lock"

    entry = entity_registry.async_get("lock.my_model_s_charger_door_lock")
    assert entry.unique_id == "tesla_model_s_111111_charger_door_lock"
