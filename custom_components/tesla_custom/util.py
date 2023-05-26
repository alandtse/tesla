"""Utilities for tesla."""

from homeassistant.helpers.httpx_client import SERVER_SOFTWARE, USER_AGENT
import httpx

try:
    import h2  # pylint: disable=unused-import # noqa: F401

    HAS_H2 = True
except ImportError:
    HAS_H2 = False


try:
    # Home Assistant 2023.4.x+
    from homeassistant.util.ssl import get_default_context

    SSL_CONTEXT = get_default_context()
except ImportError:
    from homeassistant.util.ssl import client_context

    SSL_CONTEXT = client_context()


def get_async_client():
    """Get an async client.

    http2 is preferred since it avoids the overhead of setting up multiple
    TLS connections which can reduce the chance of hitting a timeout.
    """
    return httpx.AsyncClient(
        headers={USER_AGENT: SERVER_SOFTWARE},
        timeout=60,
        verify=SSL_CONTEXT,
        http2=HAS_H2,
    )
