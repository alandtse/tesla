"""Utilities for tesla."""

import ssl

import httpx

try:
    # Home Assistant 2023.4.x+
    from homeassistant.util.ssl import get_default_context

    SSL_CONTEXT = get_default_context()
except ImportError:
    from homeassistant.util.ssl import client_context

    SSL_CONTEXT = client_context()


def create_tesla_ssl_context() -> ssl.SSLContext:
    """Return a fresh SSL context capped at TLS 1.2 for each caller.

    A module-level shared context would be mutated by every async_setup_entry
    call, causing the last loaded CA certificate to overwrite all earlier
    entries. Using a factory ensures each account gets its own isolated
    context object.
    """
    ctx = httpx.create_ssl_context()
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    return ctx
