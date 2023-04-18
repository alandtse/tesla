"""Utilities for tesla."""

try:
    # Home Assistant 2023.4.x+
    from homeassistant.util.ssl import get_default_context

    SSL_CONTEXT = get_default_context()
except ImportError:
    from homeassistant.util.ssl import client_context

    SSL_CONTEXT = client_context()


def km_to_miles(odometer: float) -> float:
    """Convert KM to Miles.

    The Tesla API natively returns the Odometer in Miles.
    TeslaMate returns the Odometer in KMs.
    We need to convert to Miles so the Odometer sensor calculates
    properly.
    """

    # conversion factor
    conv_fac = 0.621371
    miles = float(odometer) * conv_fac

    return miles
