from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from app.core.config import PLANET_SEQUENCE, SIGNS
from app.core.input_schema import UserInput


@dataclass(frozen=True)
class ChangePoint:
    date: date
    planet: str
    event_type: str
    summary: str

    def to_dict(self) -> dict:
        return {
            "date": self.date.isoformat(),
            "planet": self.planet,
            "event_type": self.event_type,
            "summary": self.summary,
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
    seed = (
        user_input.birth_date.year
        + user_input.birth_date.month
        + user_input.birth_date.day
        + user_input.birth_time.hour
        + user_input.birth_time.minute
    )

    placements = []
    for index, planet in enumerate(PLANET_SEQUENCE):
        placements.append(
            {
                "planet": planet,
                "sign": SIGNS[(seed + (index * 2)) % len(SIGNS)],
                "house": ((seed + index) % 12) + 1,
            }
        )

    return {
        "engine_mode": "placeholder",
        "zodiac": user_input.preferences.zodiac,
        "ayanamsa": user_input.preferences.ayanamsa,
        "house_system": user_input.preferences.house_system,
        "node_type": user_input.preferences.node_type,
        "ascendant": SIGNS[seed % len(SIGNS)],
        "placements": placements,
    }


def build_year_change_points(user_input: UserInput, window_start: date, window_end: date) -> list[ChangePoint]:
    del user_input

    event_types = ["ingress", "retrograde", "station", "eclipse", "node"]
    offsets = [0, 35, 74, 118, 161, 205, 248, 292, 334]
    change_points: list[ChangePoint] = []

    for index, offset in enumerate(offsets):
        event_date = window_start + timedelta(days=offset)
        if not (window_start < event_date < window_end):
            continue

        planet = PLANET_SEQUENCE[index % len(PLANET_SEQUENCE)]
        event_type = event_types[index % len(event_types)]
        change_points.append(
            ChangePoint(
                date=event_date,
                planet=planet,
                event_type=event_type,
                summary=f"Placeholder {planet.lower()} {event_type} boundary.",
            )
        )

    return change_points

