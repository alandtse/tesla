"""Tests for the Tesla update."""
from unittest.mock import patch

from homeassistant.components.update import DOMAIN as UPDATE_DOMAIN

# from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, UPDATE_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("update.my_model_s_software_update")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_software_update"


async def test_software_update_properties(hass: HomeAssistant) -> None:
    """Tests software update properties."""
    await setup_platform(hass, UPDATE_DOMAIN)

    version = car_mock_data.VEHICLE_DATA["vehicle_state"]["software_update"]["version"]

    state = hass.states.get("update.my_model_s_software_update")
    # assert state.state == str(car_mock_data.VEHICLE_STATE["software_update"])

    assert state.attributes.get("latest_version") == version

    assert (
        state.attributes.get("release_url")
        == f"https://www.notateslaapp.com/software-updates/version/{version}/release-notes"
    )


# async def test_install(hass: HomeAssistant) -> None:
#     """Tests install update."""
#     await setup_platform(hass, UPDATE_DOMAIN)

#     with patch(
#         "teslajsonpy.car.TeslaCar.schedule_software_update"
#     ) as mock_schedule_software_update:

#         assert await hass.services.async_call(
#             UPDATE_DOMAIN,
#             "install",
#             {ATTR_ENTITY_ID: "update.my_model_s_software_update"},
#             blocking=True,
#         )
#         mock_schedule_software_update.assert_awaited_once()
