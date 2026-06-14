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


TESLA_SSL_CONTEXT = httpx.create_ssl_context()
TESLA_SSL_CONTEXT.maximum_version = ssl.TLSVersion.TLSv1_2
