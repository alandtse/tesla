"""Tests for the Tesla climate."""
from unittest.mock import patch

from homeassistant.components.media_player import (
    DOMAIN as MEDIA_PLAYER_DOMAIN,
    MediaPlayerState,
)
from homeassistant.const import ATTR_ENTITY_ID, ATTR_TEMPERATURE, STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data

DEVICE_ID = "media_player.my_model_s_media_player"


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, MEDIA_PLAYER_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get(DEVICE_ID)
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_media_player"


async def test_media_player_properties(hass: HomeAssistant) -> None:
    """Tests car media player properties."""
    await setup_platform(hass, MEDIA_PLAYER_DOMAIN)

    state = hass.states.get(DEVICE_ID)

    assert state.state == MediaPlayerState.OFF

    # assert state.media_duration == car_mock_data.VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_duration"] * 1000
    # assert state.media_position == car_mock_data.VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_elapsed"] * 1000
    # assert state.media_title == car_mock_data.VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_title"]
    # assert state.media_artist == car_mock_data.VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_artist"]
    # assert state.media_album_name == car_mock_data.VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_album"]


async def test_async_media_previous_track(hass: HomeAssistant) -> None:
    """Test the async_media_previous_track method."""
    await setup_platform(hass, MEDIA_PLAYER_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.previous_track") as mock_previous_track:
        # Call the async_media_previous_track service
        assert await hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            "media_previous_track",
            {ATTR_ENTITY_ID: DEVICE_ID},
            blocking=True,
        )

        # Assert that the TeslaCar's previous_track method was called once
        mock_previous_track.assert_awaited_once()


async def test_async_media_next_track(hass: HomeAssistant) -> None:
    """Test the async_media_next_track method."""
    await setup_platform(hass, MEDIA_PLAYER_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.next_track") as mock_next_track:
        # Call the async_media_next_track service
        assert await hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            "media_next_track",
            {ATTR_ENTITY_ID: DEVICE_ID},
            blocking=True,
        )

        # Assert that the TeslaCar's next_track method was called once
        mock_next_track.assert_awaited_once()


async def test_async_set_volume_level(hass: HomeAssistant) -> None:
    """Test the async_set_volume_level method."""
    await setup_platform(hass, MEDIA_PLAYER_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.adjust_volume") as mock_adjust_volume:
        # Call the async_set_volume_level service
        assert await hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            "volume_set",
            {
                ATTR_ENTITY_ID: DEVICE_ID,
                "volume_level": 0.75,
            },
            blocking=True,
        )

        # Assert that the TeslaCar's set_volume_level method was called once with the correct argument
        mock_adjust_volume.assert_awaited_once_with(7)


async def test_async_media_pause_calls_toggle_playback(hass: HomeAssistant) -> None:
    """Test the async_media_pause method."""
    await setup_platform(hass, MEDIA_PLAYER_DOMAIN)

    with patch(
        "teslajsonpy.car.TeslaCar.toggle_playback"
    ) as mock_toggle_playback, patch(
        "teslajsonpy.car.TeslaCar.media_playback_status", "Playing"
    ):
        # Call the async_media_pause service
        assert await hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            "media_pause",
            {
                ATTR_ENTITY_ID: DEVICE_ID,
            },
            blocking=True,
        )

        # Assert that the TeslaCar's toggle_playback method was called once
        mock_toggle_playback.assert_awaited_once()


async def test_async_media_play_calls_toggle_playback(hass: HomeAssistant) -> None:
    """Test the async_media_play method."""
    await setup_platform(hass, MEDIA_PLAYER_DOMAIN)

    with patch(
        "teslajsonpy.car.TeslaCar.toggle_playback"
    ) as mock_toggle_playback, patch(
        "teslajsonpy.car.TeslaCar.media_playback_status", "Paused"
    ):
        # Call the async_media_play service
        assert await hass.services.async_call(
            MEDIA_PLAYER_DOMAIN,
            "media_play",
            {
                ATTR_ENTITY_ID: DEVICE_ID,
            },
            blocking=True,
        )

        # Assert that the TeslaCar's toggle_playback method was called once
        mock_toggle_playback.assert_awaited_once()
