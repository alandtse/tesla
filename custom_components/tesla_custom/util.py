"""Utilities for tesla."""

import ssl

try:
    # Home Assistant 2023.4.x+
    from homeassistant.util.ssl import get_default_context

    SSL_CONTEXT = get_default_context()
except ImportError:
    from homeassistant.util.ssl import client_context

    SSL_CONTEXT = client_context()


SSL_CONTEXT.minimum_version = ssl.TLSVersion.TLSv1_3
SSL_CONTEXT.maximum_version = ssl.TLSVersion.TLSv1_3
