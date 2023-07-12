"""Support for Tesla Media Player."""

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.core import HomeAssistant
from teslajsonpy.car import TeslaCar

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, config_entry, async_add_entities
) -> None:
    """Set up the Tesla climate by config_entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinators = entry_data["coordinators"]
    cars = entry_data["cars"]

    entities = [
        TeslaCarMediaPlayer(
            hass,
            car,
            coordinators[vin],
        )
        for vin, car in cars.items()
    ]
    async_add_entities(entities, update_before_add=True)


class TeslaCarMediaPlayer(TeslaCarEntity, MediaPlayerEntity):
    """Representation of a Tesla Media Player."""

    _attr_supported_features = (
        MediaPlayerEntityFeature.PAUSE
        | MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.PREVIOUS_TRACK
        | MediaPlayerEntityFeature.NEXT_TRACK
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_STEP
    )

    _attr_device_class = MediaPlayerDeviceClass.SPEAKER

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize Media Player entity."""
        super().__init__(hass, car, coordinator)
        self.type = "media player"

    @property
    def state(self) -> MediaPlayerState | None:
        """Return the state of the player."""
        if self._car.media_playback_status == "Stopped":
            return MediaPlayerState.OFF
        if self._car.media_playback_status == "Playing":
            return MediaPlayerState.PLAYING
        if self._car.media_playback_status == "Paused":
            return MediaPlayerState.PAUSED

        return None

    @property
    def volume_level(self) -> float | None:
        """Volume level of the media player (0..1)."""
        if self._car.data_available:
            max_vol = self._car.audio_volume_max
            current_volume = self._car.audio_volume
            normalized_volume = current_volume / max_vol

            return normalized_volume
        return None

    @property
    def media_duration(self) -> int | None:
        """Duration of current playing media in seconds."""
        if (duration := self._car.now_playing_duration) is not None:
            return duration / 1000
        return None

    @property
    def media_position(self) -> int | None:
        """Position of current playing media in seconds."""
        if (position := self._car.now_playing_elapsed) is not None:
            return position / 1000
        return None

    @property
    def media_title(self):
        """Title of current playing media."""
        return self._car.now_playing_title

    @property
    def media_artist(self):
        """Artist of current playing media (Music track only)."""
        return self._car.now_playing_artist

    @property
    def media_album_name(self):
        """Album of current playing media (Music track only)."""
        return self._car.now_playing_album

    async def async_media_pause(self) -> None:
        """Send pause command."""
        if self.state == MediaPlayerState.PLAYING:
            await self._car.toggle_playback()

    async def async_media_play(self) -> None:
        """Send play command."""
        if self.state != MediaPlayerState.PLAYING:
            await self._car.toggle_playback()

    async def async_media_previous_track(self) -> None:
        """Send previous track command."""
        await self._car.previous_track()

    async def async_media_next_track(self) -> None:
        """Send next track command."""
        await self._car.next_track()

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        if self._car.data_available:
            max_vol = self._car.audio_volume_max
            normalized_volume = volume * max_vol

            await self._car.adjust_volume(int(normalized_volume))
