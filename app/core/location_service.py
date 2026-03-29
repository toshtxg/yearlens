from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from app.core.input_schema import UserInput


@dataclass(frozen=True)
class LocationContext:
    query: str
    resolved_name: str
    latitude: float
    longitude: float
    timezone_id: str
    source: str


_TIMEZONE_FINDER = TimezoneFinder(in_memory=True)


def resolve_location_context(user_input: UserInput) -> LocationContext:
    if _has_partial_coordinates(user_input):
        raise ValueError("Provide both latitude and longitude, or leave both blank.")

    if user_input.birth_latitude is not None and user_input.birth_longitude is not None:
        latitude = float(user_input.birth_latitude)
        longitude = float(user_input.birth_longitude)
        resolved_name = user_input.birth_location
        source = "manual_coordinates"
    else:
        latitude, longitude, resolved_name = _geocode_location(user_input.birth_location)
        source = "geocoded_nominatim"

    timezone_id = user_input.timezone_id or _lookup_timezone(latitude, longitude)
    try:
        ZoneInfo(timezone_id)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Unsupported timezone ID: {timezone_id}") from exc

    return LocationContext(
        query=user_input.birth_location,
        resolved_name=resolved_name,
        latitude=latitude,
        longitude=longitude,
        timezone_id=timezone_id,
        source=source if user_input.timezone_id is None else f"{source}+manual_timezone",
    )


def _has_partial_coordinates(user_input: UserInput) -> bool:
    return (user_input.birth_latitude is None) ^ (user_input.birth_longitude is None)


@lru_cache(maxsize=256)
def _geocode_location(query: str) -> tuple[float, float, str]:
    geocoder = Nominatim(user_agent=os.getenv("GEOCODER_USER_AGENT", "yearlens-app"), timeout=10)
    location = geocoder.geocode(query, exactly_one=True, addressdetails=True)
    if location is None:
        raise ValueError(
            "Could not resolve the birth location. Try a more specific place name or provide latitude/longitude manually."
        )

    resolved_name = location.address or query
    return float(location.latitude), float(location.longitude), resolved_name


@lru_cache(maxsize=256)
def _lookup_timezone(latitude: float, longitude: float) -> str:
    timezone_id = _TIMEZONE_FINDER.timezone_at(lng=longitude, lat=latitude)
    if timezone_id is None:
        raise ValueError("Could not resolve a timezone for the provided coordinates.")
    return timezone_id
