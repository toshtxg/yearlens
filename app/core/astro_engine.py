from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import swisseph as swe

from app.core.config import PLANET_SEQUENCE, SIGNS
from app.core.input_schema import UserInput
from app.core.location_service import LocationContext, resolve_location_context

AYANAMSA_MAP = {
    "lahiri": swe.SIDM_LAHIRI,
}

PLANET_IDS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
}

TRANSIT_PLANETS = ["Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]
STATION_PLANETS = {"Mercury", "Venus", "Mars", "Jupiter", "Saturn"}
EVENT_INTENSITY = {
    ("Sun", "ingress"): 1,
    ("Mercury", "ingress"): 1,
    ("Venus", "ingress"): 1,
    ("Mars", "ingress"): 2,
    ("Jupiter", "ingress"): 3,
    ("Saturn", "ingress"): 3,
    ("Rahu", "ingress"): 3,
    ("Ketu", "ingress"): 3,
    ("Mercury", "station"): 2,
    ("Venus", "station"): 2,
    ("Mars", "station"): 3,
    ("Jupiter", "station"): 4,
    ("Saturn", "station"): 4,
    ("Sun", "eclipse"): 5,
    ("Moon", "eclipse"): 5,
}


@dataclass(frozen=True)
class BodyState:
    longitude: float
    sign: str
    sign_index: int
    house: int
    speed: float
    motion: str


@dataclass(frozen=True)
class ChangePoint:
    date: date
    planet: str
    event_type: str
    summary: str
    sign: str | None = None
    house: int | None = None
    longitude: float | None = None
    speed: float | None = None
    motion: str | None = None
    intensity: int = 1

    def to_dict(self) -> dict:
        return {
            "date": self.date.isoformat(),
            "planet": self.planet,
            "event_type": self.event_type,
            "summary": self.summary,
            "sign": self.sign,
            "house": self.house,
            "longitude": self.longitude,
            "speed": self.speed,
            "motion": self.motion,
            "intensity": self.intensity,
        }


def _coerce_anniversary(source_date: date, year: int) -> date:
    if source_date.month == 2 and source_date.day == 29:
        return date(year, 2, 28)
    return date(year, source_date.month, source_date.day)


def get_year_window(user_input: UserInput) -> tuple[date, date]:
    if user_input.year_anchor == "calendar":
        return date(user_input.target_year, 1, 1), date(user_input.target_year, 12, 31)

    start = _coerce_anniversary(user_input.birth_date, user_input.target_year)
    end = _coerce_anniversary(user_input.birth_date, user_input.target_year + 1) - timedelta(days=1)
    return start, end


def build_natal_chart(user_input: UserInput) -> dict:
    location = resolve_location_context(user_input)
    flags = _build_calc_flags(user_input)
    birth_utc = _birth_datetime_utc(user_input, location)
    jd_et, jd_ut = swe.utc_to_jd(
        birth_utc.year,
        birth_utc.month,
        birth_utc.day,
        birth_utc.hour,
        birth_utc.minute,
        birth_utc.second + (birth_utc.microsecond / 1_000_000),
    )
    asc_longitude = _ascendant_longitude(jd_ut, location, user_input, flags)

    warnings: set[str] = set()
    placements = []
    for planet in PLANET_SEQUENCE:
        body = _body_state(jd_ut, planet, user_input, asc_longitude, flags)
        message = _body_warning(jd_ut, planet, user_input, flags)
        if message:
            warnings.add(message)
        placements.append(
            {
                "planet": planet,
                "sign": body.sign,
                "house": body.house,
                "longitude": round(body.longitude, 4),
                "sign_degree": round(body.longitude % 30, 4),
                "speed": round(body.speed, 6),
                "motion": body.motion,
            }
        )

    backend = "moshier_fallback" if any("Moshier" in warning for warning in warnings) else "swisseph_files"
    return {
        "engine_mode": "swisseph",
        "ephemeris_backend": backend,
        "warnings": sorted(warnings),
        "zodiac": user_input.preferences.zodiac,
        "ayanamsa": user_input.preferences.ayanamsa,
        "ayanamsa_value": round(swe.get_ayanamsa_ut(jd_ut), 6),
        "house_system": user_input.preferences.house_system,
        "node_type": user_input.preferences.node_type,
        "ascendant": {
            "sign": _sign_name(asc_longitude),
            "longitude": round(asc_longitude, 4),
        },
        "birth": {
            "local_datetime": _birth_datetime_local(user_input, location).isoformat(),
            "utc_datetime": birth_utc.isoformat(),
            "jd_ut": jd_ut,
            "jd_et": jd_et,
        },
        "location": {
            "query": location.query,
            "resolved_name": location.resolved_name,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timezone_id": location.timezone_id,
            "source": location.source,
        },
        "placements": placements,
    }


def build_year_change_points(
    user_input: UserInput,
    natal_chart: dict,
    window_start: date,
    window_end: date,
) -> list[ChangePoint]:
    flags = _build_calc_flags(user_input)
    location = LocationContext(
        query=natal_chart["location"]["query"],
        resolved_name=natal_chart["location"]["resolved_name"],
        latitude=natal_chart["location"]["latitude"],
        longitude=natal_chart["location"]["longitude"],
        timezone_id=natal_chart["location"]["timezone_id"],
        source=natal_chart["location"]["source"],
    )
    asc_longitude = float(natal_chart["ascendant"]["longitude"])

    change_points: list[ChangePoint] = []
    previous_by_planet: dict[str, BodyState] = {}
    cursor = window_start

    while cursor <= window_end:
        jd_ut = _local_date_to_jd_ut(cursor, location.timezone_id)
        for planet in TRANSIT_PLANETS:
            current = _body_state(jd_ut, planet, user_input, asc_longitude, flags)
            previous = previous_by_planet.get(planet)
            if previous is not None:
                if current.sign_index != previous.sign_index:
                    change_points.append(
                        ChangePoint(
                            date=cursor,
                            planet=planet,
                            event_type="ingress",
                            summary=f"{planet} enters {current.sign} and activates house {current.house}.",
                            sign=current.sign,
                            house=current.house,
                            longitude=round(current.longitude, 4),
                            speed=round(current.speed, 6),
                            motion=current.motion,
                            intensity=_event_intensity(planet, "ingress"),
                        )
                    )
                if planet in STATION_PLANETS and current.motion != previous.motion:
                    change_points.append(
                        ChangePoint(
                            date=cursor,
                            planet=planet,
                            event_type="station",
                            summary=f"{planet} stations {current.motion} in {current.sign}, emphasizing house {current.house}.",
                            sign=current.sign,
                            house=current.house,
                            longitude=round(current.longitude, 4),
                            speed=round(current.speed, 6),
                            motion=current.motion,
                            intensity=_event_intensity(planet, "station"),
                        )
                    )
            previous_by_planet[planet] = current
        cursor += timedelta(days=1)

    change_points.extend(_build_eclipse_events(window_start, window_end, location, user_input, asc_longitude, flags))
    return _deduplicate_change_points(change_points)


def _build_calc_flags(user_input: UserInput) -> int:
    ayanamsa = AYANAMSA_MAP.get(user_input.preferences.ayanamsa.lower())
    if ayanamsa is None:
        raise ValueError(f"Unsupported ayanamsa: {user_input.preferences.ayanamsa}")

    ephe_path = os.getenv("SWISSEPH_EPHE_PATH")
    if ephe_path:
        swe.set_ephe_path(ephe_path)

    swe.set_sid_mode(ayanamsa)
    return swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL


def _birth_datetime_local(user_input: UserInput, location: LocationContext) -> datetime:
    return datetime.combine(
        user_input.birth_date,
        user_input.birth_time,
        tzinfo=ZoneInfo(location.timezone_id),
    )


def _birth_datetime_utc(user_input: UserInput, location: LocationContext) -> datetime:
    return _birth_datetime_local(user_input, location).astimezone(ZoneInfo("UTC"))


def _local_date_to_jd_ut(local_date: date, timezone_id: str) -> float:
    local_dt = datetime.combine(local_date, time(12, 0), tzinfo=ZoneInfo(timezone_id))
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))
    _, jd_ut = swe.utc_to_jd(
        utc_dt.year,
        utc_dt.month,
        utc_dt.day,
        utc_dt.hour,
        utc_dt.minute,
        utc_dt.second + (utc_dt.microsecond / 1_000_000),
    )
    return jd_ut


def _jd_ut_to_local_date(jd_ut: float, timezone_id: str) -> date:
    year, month, day, hour = swe.revjul(jd_ut, swe.GREG_CAL)
    hours = int(hour)
    minutes = int((hour - hours) * 60)
    seconds_float = ((hour - hours) * 60 - minutes) * 60
    seconds = int(seconds_float)
    microseconds = int(round((seconds_float - seconds) * 1_000_000))

    utc_dt = datetime(year, month, day, hours, minutes, seconds, microseconds, tzinfo=ZoneInfo("UTC"))
    return utc_dt.astimezone(ZoneInfo(timezone_id)).date()


def _ascendant_longitude(jd_ut: float, location: LocationContext, user_input: UserInput, flags: int) -> float:
    if user_input.preferences.house_system != "whole_sign":
        raise ValueError(f"Unsupported house system: {user_input.preferences.house_system}")

    _, ascmc = swe.houses_ex(jd_ut, location.latitude, location.longitude, b"W", flags)
    return float(ascmc[0])


def _body_state(jd_ut: float, planet: str, user_input: UserInput, asc_longitude: float, flags: int) -> BodyState:
    longitude, speed = _planet_longitude_and_speed(jd_ut, planet, user_input, flags)
    sign_index = int(longitude // 30)
    return BodyState(
        longitude=longitude,
        sign=SIGNS[sign_index],
        sign_index=sign_index,
        house=_whole_sign_house(longitude, asc_longitude),
        speed=speed,
        motion="retrograde" if speed < 0 else "direct",
    )


def _planet_longitude_and_speed(user_input_jd: float, planet: str, user_input: UserInput, flags: int) -> tuple[float, float]:
    if planet in PLANET_IDS:
        xx, _, _ = swe.calc_ut(user_input_jd, PLANET_IDS[planet], flags)
        return float(xx[0] % 360), float(xx[3])

    node_id = swe.TRUE_NODE if user_input.preferences.node_type == "true" else swe.MEAN_NODE
    xx, _, _ = swe.calc_ut(user_input_jd, node_id, flags)
    longitude = float(xx[0] % 360)
    if planet == "Rahu":
        return longitude, float(xx[3])
    if planet == "Ketu":
        return (longitude + 180.0) % 360, float(xx[3])

    raise ValueError(f"Unsupported planet: {planet}")


def _body_warning(jd_ut: float, planet: str, user_input: UserInput, flags: int) -> str:
    if planet in PLANET_IDS:
        _, _, message = swe.calc_ut(jd_ut, PLANET_IDS[planet], flags)
        return message.strip()

    node_id = swe.TRUE_NODE if user_input.preferences.node_type == "true" else swe.MEAN_NODE
    _, _, message = swe.calc_ut(jd_ut, node_id, flags)
    return message.strip()


def _whole_sign_house(longitude: float, asc_longitude: float) -> int:
    body_sign = int(longitude // 30)
    asc_sign = int(asc_longitude // 30)
    return ((body_sign - asc_sign) % 12) + 1


def _sign_name(longitude: float) -> str:
    return SIGNS[int((longitude % 360) // 30)]


def _event_intensity(planet: str, event_type: str) -> int:
    return EVENT_INTENSITY.get((planet, event_type), 1)


def _build_eclipse_events(
    window_start: date,
    window_end: date,
    location: LocationContext,
    user_input: UserInput,
    asc_longitude: float,
    flags: int,
) -> list[ChangePoint]:
    events: list[ChangePoint] = []
    start_jd = _local_date_to_jd_ut(window_start - timedelta(days=1), location.timezone_id)
    end_jd = _local_date_to_jd_ut(window_end + timedelta(days=1), location.timezone_id)

    search_jd = start_jd
    while True:
        _, tret = swe.sol_eclipse_when_glob(search_jd, swe.FLG_SWIEPH)
        event_jd = float(tret[0])
        if event_jd > end_jd:
            break

        event_date = _jd_ut_to_local_date(event_jd, location.timezone_id)
        if window_start <= event_date <= window_end:
            body = _body_state(event_jd, "Sun", user_input, asc_longitude, flags)
            events.append(
                ChangePoint(
                    date=event_date,
                    planet="Sun",
                    event_type="eclipse",
                    summary=f"Solar eclipse in {body.sign}, highlighting house {body.house}.",
                    sign=body.sign,
                    house=body.house,
                    longitude=round(body.longitude, 4),
                    speed=round(body.speed, 6),
                    motion=body.motion,
                    intensity=_event_intensity("Sun", "eclipse"),
                )
            )
        search_jd = event_jd + 10

    search_jd = start_jd
    while True:
        _, tret = swe.lun_eclipse_when(search_jd, swe.FLG_SWIEPH)
        event_jd = float(tret[0])
        if event_jd > end_jd:
            break

        event_date = _jd_ut_to_local_date(event_jd, location.timezone_id)
        if window_start <= event_date <= window_end:
            body = _body_state(event_jd, "Moon", user_input, asc_longitude, flags)
            events.append(
                ChangePoint(
                    date=event_date,
                    planet="Moon",
                    event_type="eclipse",
                    summary=f"Lunar eclipse in {body.sign}, highlighting house {body.house}.",
                    sign=body.sign,
                    house=body.house,
                    longitude=round(body.longitude, 4),
                    speed=round(body.speed, 6),
                    motion=body.motion,
                    intensity=_event_intensity("Moon", "eclipse"),
                )
            )
        search_jd = event_jd + 10

    return events


def _deduplicate_change_points(change_points: list[ChangePoint]) -> list[ChangePoint]:
    unique: dict[tuple[date, str, str, str], ChangePoint] = {}
    for point in sorted(change_points, key=lambda item: (item.date, item.planet, item.event_type, item.summary)):
        unique[(point.date, point.planet, point.event_type, point.summary)] = point
    return list(unique.values())
