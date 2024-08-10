"""Support for Tesla cars."""

import asyncio
from datetime import timedelta
from functools import partial
from http import HTTPStatus
import logging
import ssl
from typing import Any

import async_timeout
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_CLIENT_ID,
    CONF_DOMAIN,
    CONF_SCAN_INTERVAL,
    CONF_TOKEN,
    CONF_USERNAME,
    EVENT_HOMEASSISTANT_CLOSE,
)
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.httpx_client import SERVER_SOFTWARE, USER_AGENT
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import httpx
from teslajsonpy import Controller as TeslaAPI
from teslajsonpy.const import AUTH_DOMAIN
from teslajsonpy.exceptions import IncompleteCredentials, TeslaException

from .config_flow import CannotConnect, InvalidAuth, validate_input
from .const import (
    CONF_API_PROXY_CERT,
    CONF_API_PROXY_URL,
    CONF_ENABLE_TESLAMATE,
    CONF_EXPIRATION,
    CONF_INCLUDE_ENERGYSITES,
    CONF_INCLUDE_VEHICLES,
    CONF_POLLING_POLICY,
    CONF_WAKE_ON_START,
    DATA_LISTENER,
    DEFAULT_ENABLE_TESLAMATE,
    DEFAULT_POLLING_POLICY,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_WAKE_ON_START,
    DOMAIN,
    MIN_SCAN_INTERVAL,
    PLATFORMS,
)
from .services import async_setup_services, async_unload_services
from .teslamate import TeslaMate
from .util import SSL_CONTEXT

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


@callback
def _async_save_tokens(hass, config_entry, access_token, refresh_token, expiration):
    hass.config_entries.async_update_entry(
        config_entry,
        data={
            **config_entry.data,
            CONF_ACCESS_TOKEN: access_token,
            CONF_TOKEN: refresh_token,
            CONF_EXPIRATION: expiration,
        },
    )


@callback
def _async_configured_emails(hass):
    """Return a set of configured Tesla emails."""
    return {
        entry.data[CONF_USERNAME]
        for entry in hass.config_entries.async_entries(DOMAIN)
        if CONF_USERNAME in entry.data
    }


async def async_setup(hass, base_config):
    """Set up of Tesla component."""

    def _update_entry(email, data=None, options=None):
        data = data or {}
        options = options or {
            CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
            CONF_WAKE_ON_START: DEFAULT_WAKE_ON_START,
            CONF_POLLING_POLICY: DEFAULT_POLLING_POLICY,
        }
        for entry in hass.config_entries.async_entries(DOMAIN):
            if email != entry.title:
                continue
            hass.config_entries.async_update_entry(entry, data=data, options=options)

    config = base_config.get(DOMAIN)

    if not config:
        return True

    email = config[CONF_USERNAME]
    token = config[CONF_TOKEN]
    scan_interval = config[CONF_SCAN_INTERVAL]

    if email in _async_configured_emails(hass):
        try:
            info = await validate_input(hass, config)
        except (CannotConnect, InvalidAuth):
            return False
        _update_entry(
            email,
            data={
                CONF_USERNAME: email,
                CONF_ACCESS_TOKEN: info[CONF_ACCESS_TOKEN],
                CONF_TOKEN: info[CONF_TOKEN],
                CONF_EXPIRATION: info[CONF_EXPIRATION],
            },
            options={CONF_SCAN_INTERVAL: scan_interval},
        )
    else:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": SOURCE_IMPORT},
                data={CONF_USERNAME: email, CONF_TOKEN: token},
            )
        )
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][email] = {CONF_SCAN_INTERVAL: scan_interval}

    return True


async def async_setup_entry(hass, config_entry):
    """Set up Tesla as config entry."""
    # pylint: disable=too-many-locals,too-many-statements,too-many-branches
    hass.data.setdefault(DOMAIN, {})
    config = config_entry.data
    # Because users can have multiple accounts, we always
    # create a new session so they have separate cookies

    if api_proxy_cert := config.get(CONF_API_PROXY_CERT):
        try:
            await hass.async_add_executor_job(
                SSL_CONTEXT.load_verify_locations, api_proxy_cert
            )
            if _LOGGER.isEnabledFor(logging.DEBUG):
                _LOGGER.debug("Trusting CA: %s", SSL_CONTEXT.get_ca_certs()[-1])
        except (FileNotFoundError, ssl.SSLError):
            _LOGGER.warning(
                "Unable to load custom SSL certificate from %s",
                api_proxy_cert,
            )

    async_client = httpx.AsyncClient(
        headers={USER_AGENT: SERVER_SOFTWARE}, timeout=60, verify=SSL_CONTEXT
    )
    email = config_entry.title

    if not hass.data[DOMAIN]:
        async_setup_services(hass)

    if email in hass.data[DOMAIN] and CONF_SCAN_INTERVAL in hass.data[DOMAIN][email]:
        scan_interval = hass.data[DOMAIN][email][CONF_SCAN_INTERVAL]
        hass.config_entries.async_update_entry(
            config_entry, options={CONF_SCAN_INTERVAL: scan_interval}
        )
        hass.data[DOMAIN].pop(email)

    try:
        controller = TeslaAPI(
            async_client,
            email=config.get(CONF_USERNAME),
            refresh_token=config[CONF_TOKEN],
            access_token=config[CONF_ACCESS_TOKEN],
            expiration=config.get(CONF_EXPIRATION, 0),
            auth_domain=config.get(CONF_DOMAIN, AUTH_DOMAIN),
            update_interval=config_entry.options.get(
                CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
            ),
            polling_policy=config_entry.options.get(
                CONF_POLLING_POLICY, DEFAULT_POLLING_POLICY
            ),
            api_proxy_url=config.get(CONF_API_PROXY_URL),
            client_id=config.get(CONF_CLIENT_ID),
        )
        result = await controller.connect(
            include_vehicles=config.get(CONF_INCLUDE_VEHICLES),
            include_energysites=config.get(CONF_INCLUDE_ENERGYSITES),
        )
        refresh_token = result["refresh_token"]
        access_token = result["access_token"]
        expiration = result["expiration"]

    except IncompleteCredentials as ex:
        await async_client.aclose()
        raise ConfigEntryAuthFailed from ex

    except (httpx.ConnectTimeout, httpx.ConnectError) as ex:
        await async_client.aclose()
        raise ConfigEntryNotReady from ex

    except TeslaException as ex:
        await async_client.aclose()

        if ex.code == HTTPStatus.UNAUTHORIZED:
            raise ConfigEntryAuthFailed from ex

        if ex.message in [
            "TOO_MANY_REQUESTS",
            "UPSTREAM_TIMEOUT",
        ]:
            raise ConfigEntryNotReady(
                f"Temporarily unable to communicate with Tesla API: {ex.message}"
            ) from ex

        _LOGGER.error("Unable to communicate with Tesla API: %s", ex.message)

        return False

    async def _async_close_client(*_):
        await async_client.aclose()

    @callback
    def _async_create_close_task():
        # Background tasks are tracked in HA to prevent them from
        # being garbage collected in the middle of the task since
        # asyncio only holds a weak reference to them.
        #
        # https://docs.python.org/3/library/asyncio-task.html#creating-tasks

        if hasattr(hass, "async_create_background_task"):
            hass.async_create_background_task(
                _async_close_client(), "tesla_close_client"
            )
        else:
            asyncio.create_task(_async_close_client())

    config_entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_CLOSE, _async_close_client)
    )
    config_entry.async_on_unload(_async_create_close_task)

    _async_save_tokens(hass, config_entry, access_token, refresh_token, expiration)

    try:
        if config_entry.data.get("initial_setup"):
            wake_if_asleep = True
        else:
            wake_if_asleep = config_entry.options.get(
                CONF_WAKE_ON_START, DEFAULT_WAKE_ON_START
            )

        cars = await controller.generate_car_objects(wake_if_asleep=wake_if_asleep)

        hass.config_entries.async_update_entry(
            config_entry, data={**config_entry.data, "initial_setup": False}
        )

    except TeslaException as ex:
        await async_client.aclose()

        if ex.message in [
            "TOO_MANY_REQUESTS",
            "SERVICE_MAINTENANCE",
            "UPSTREAM_TIMEOUT",
        ]:
            raise ConfigEntryNotReady(
                f"Temporarily unable to communicate with Tesla API: {ex.message}"
            ) from ex

        _LOGGER.error("Unable to communicate with Tesla API: %s", ex.message)

        return False

    try:
        energysites = await controller.generate_energysite_objects()

    except TeslaException as ex:
        await async_client.aclose()

        if ex.message in [
            "TOO_MANY_REQUESTS",
            "SERVICE_MAINTENANCE",
            "UPSTREAM_TIMEOUT",
        ]:
            raise ConfigEntryNotReady(
                f"Temporarily unable to communicate with Tesla API: {ex.message}"
            ) from ex

        _LOGGER.error("Unable to communicate with Tesla API: %s", ex.message)

        return False

    reload_lock = asyncio.Lock()
    _partial_coordinator = partial(
        TeslaDataUpdateCoordinator,
        hass,
        config_entry=config_entry,
        controller=controller,
        reload_lock=reload_lock,
        update_vehicles=False,
    )
    energy_coordinators = {
        energy_site_id: _partial_coordinator(energy_site_id=energy_site_id)
        for energy_site_id in energysites
    }
    car_coordinators = {vin: _partial_coordinator(vin=vin) for vin in cars}
    coordinators = {**energy_coordinators, **car_coordinators}

    if car_coordinators:
        update_vehicles_coordinator = _partial_coordinator(update_vehicles=True)
        coordinators["update_vehicles"] = update_vehicles_coordinator

        # If we have cars, we want to update the vehicles coordinator
        # to keep the vehicles up to date.
        @callback
        def _async_update_vehicles():
            """Update vehicles coordinator.

            This listener is called when the update_vehicles_coordinator
            is updated. Since each car coordinator is also polling we don't
            need to do anything here, but we need to have this listener
            to ensure the update_vehicles_coordinator is updated regularly.
            """

        update_vehicles_coordinator.async_add_listener(_async_update_vehicles)

    teslamate = TeslaMate(hass=hass, cars=cars, coordinators=coordinators)

    enable_teslamate = config_entry.options.get(
        CONF_ENABLE_TESLAMATE, DEFAULT_ENABLE_TESLAMATE
    )

    await teslamate.enable(enable_teslamate)

    hass.data[DOMAIN][config_entry.entry_id] = {
        "controller": controller,
        "coordinators": coordinators,
        "cars": cars,
        "energysites": energysites,
        "teslamate": teslamate,
        DATA_LISTENER: [config_entry.add_update_listener(update_listener)],
    }
    _LOGGER.debug("Connected to the Tesla API")

    # We do not do a first refresh as we already know the API is working
    # from above. Each platform will schedule a refresh via update_before_add
    # for the sites/vehicles they are interested in.

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass, config_entry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    controller: TeslaAPI = entry_data["controller"]
    await controller.disconnect()

    for listener in entry_data[DATA_LISTENER]:
        listener()
    username = config_entry.title

    await entry_data["teslamate"].unload()

    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)
        _LOGGER.debug("Unloaded entry for %s", username)

        if not hass.data[DOMAIN]:
            async_unload_services(hass)

        return True

    return False


async def update_listener(hass, config_entry):
    """Update when config_entry options update."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    controller: TeslaAPI = entry_data["controller"]
    old_update_interval = controller.update_interval
    controller.update_interval = config_entry.options.get(
        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
    )
    if old_update_interval != controller.update_interval:
        _LOGGER.debug(
            "Changing scan_interval from %s to %s",
            old_update_interval,
            controller.update_interval,
        )

    enable_teslamate = config_entry.options.get(
        CONF_ENABLE_TESLAMATE, DEFAULT_ENABLE_TESLAMATE
    )

    await entry_data["teslamate"].enable(enable_teslamate)


class TeslaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Tesla data."""

    def __init__(
        self,
        hass,
        *,
        config_entry,
        controller: TeslaAPI,
        reload_lock: asyncio.Lock,
        vin: str | None = None,
        energy_site_id: str | None = None,
        update_vehicles: bool = False,
    ) -> None:
        """Initialize global Tesla data updater."""
        self.controller = controller
        self.config_entry = config_entry
        self.reload_lock = reload_lock
        self.vin = vin
        self.vins = {vin} if vin else set()
        self.energy_site_id = energy_site_id
        self.energy_site_ids = {energy_site_id} if energy_site_id else set()
        self.update_vehicles = update_vehicles
        self._cancel_debounce_timer = None
        self._last_update_time = None
        self.last_update_time: float | None = None
        self.assumed_state = True

        update_interval = timedelta(seconds=MIN_SCAN_INTERVAL)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        controller = self.controller
        if controller.is_token_refreshed():
            # It doesn't matter which coordinator calls this, as long as there
            # are no awaits in the below code, it will be called only once.
            result = controller.get_tokens()
            refresh_token = result["refresh_token"]
            access_token = result["access_token"]
            expiration = result["expiration"]
            _async_save_tokens(
                self.hass, self.config_entry, access_token, refresh_token, expiration
            )
            _LOGGER.debug("Saving new tokens in config_entry")

        data = None
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(30):
                _LOGGER.debug("Running controller.update()")
                data = await controller.update(
                    vins=self.vins,
                    energy_site_ids=self.energy_site_ids,
                    update_vehicles=self.update_vehicles,
                )
        except IncompleteCredentials:
            if self.reload_lock.locked():
                # Any of the coordinators can trigger a reload, but we only
                # want to do it once. If the lock is already locked, we know
                # another coordinator is already reloading.
                _LOGGER.debug("Config entry is already being reloaded")
                return
            async with self.reload_lock:
                await self.hass.config_entries.async_reload(self.config_entry.entry_id)
        except TeslaException as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        else:
            if vin := self.vin:
                self.last_update_time = controller.get_last_update_time(vin=vin)
                self.assumed_state = not controller.is_car_online(vin=vin) and (
                    self.last_update_time - controller.get_last_wake_up_time(vin=vin)
                    > controller.update_interval
                )
        return data

    @callback
    def async_update_listeners_debounced(
        self, delay_since_last=0.1, max_delay=1.0
    ) -> None:
        """
        Debounced version of async_update_listeners.

        This function cancels the previous task (if any) and creates a new one.

        Parameters
        ----------
        delay_since_last : float
            Minimum delay in seconds since the last received message before calling async_update_listeners.
        max_delay : float
            Maximum delay in seconds before calling async_update_listeners,
            regardless of when the last message was received.

        """
        # If there's an existing debounce task, cancel it
        if self._cancel_debounce_timer:
            self._cancel_debounce_timer()
            _LOGGER.debug("Previous debounce task cancelled")

        # Schedule the call to _async_debounced, pass max_delay using partial
        self._cancel_debounce_timer = async_call_later(
            self.hass, delay_since_last, partial(self._async_debounced, max_delay)
        )
        _LOGGER.debug("New debounce task scheduled")

    @callback
    def _async_debounced(self, max_delay: float, *args: Any) -> None:
        """
        Debounce method that waits a certain delay since the last update.

        This method ensures that async_update_listeners is called at least every max_delay seconds.

        Parameters
        ----------
        max_delay : float
            Maximum delay in seconds before calling async_update_listeners.

        """
        # Get the current time
        now = self.hass.loop.time()

        # If it's been at least max_delay since the last update (or there was no previous update),
        # call async_update_listeners and update the last update time
        if not self._last_update_time or now - self._last_update_time >= max_delay:
            self._last_update_time = now
            self.async_update_listeners()
            _LOGGER.debug("Listeners updated")
        else:
            # If it hasn't been max_delay since the last update,
            # schedule the call to _async_debounced again after the remaining time
            self._cancel_debounce_timer = async_call_later(
                self.hass,
                max_delay - (now - self._last_update_time),
                partial(self._async_debounced, max_delay),
            )
            _LOGGER.debug("Max delay not reached, scheduling another debounce task")
