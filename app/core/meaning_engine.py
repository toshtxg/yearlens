from __future__ import annotations

from app.core.config import (
    ADVICE_BY_TONE,
    DOMAINS,
    HOUSE_DOMAIN_MAP,
    HOUSE_MEANINGS,
    PLANET_MEANINGS,
    TONE_BY_PLANET,
)
from app.core.period_engine import PeriodWindow


def build_period_meanings(periods: list[PeriodWindow], natal_chart: dict) -> list[dict]:
    payload: list[dict] = []

    for period in periods:
        driver = _dominant_driver(period.drivers)
        planet = driver.planet if driver else "Saturn"
        house = driver.house if driver and driver.house is not None else _house_for_planet(natal_chart, planet)
        tone = _tone_for_driver(driver)
        scores = {domain: 3 for domain in DOMAINS}

        for domain in HOUSE_DOMAIN_MAP.get(house, []):
            scores[domain] = min(10, scores[domain] + 4)

        if tone in {"stressful", "serious", "volatile", "reflective"}:
            scores["health_emotional"] = min(10, scores["health_emotional"] + 1)
        if tone in {"constructive", "expansive", "supportive"}:
            scores["study_growth"] = min(10, scores["study_growth"] + 1)

        top_domains = sorted(scores, key=scores.get, reverse=True)[:3]
        advice = _build_advice(tone, top_domains)
        driver_payload = {
            "planet": planet,
            "house": house,
            "sign": driver.sign if driver else None,
            "event_type": driver.event_type if driver else "fallback",
            "summary": driver.summary if driver else "Fallback driver used because no major transit event was attached to this period.",
            "planet_meaning": ", ".join(PLANET_MEANINGS[planet][:2]),
            "house_meaning": ", ".join(HOUSE_MEANINGS[house][:2]),
            "combined_effect": _combined_effect(planet, house, tone, driver),
        }

        payload.append(
            {
                "id": period.id,
                "start_date": period.start_date.isoformat(),
                "end_date": period.end_date.isoformat(),
                "tone": tone,
                "domains": scores,
                "advice": advice,
                "drivers": [driver_payload],
                "top_domains": top_domains,
                "driver_summary": driver_payload["summary"],
                "confidence": round(_confidence_score(period), 2),
            }
        )

    return payload


def _house_for_planet(natal_chart: dict, planet: str) -> int:
    for placement in natal_chart.get("placements", []):
        if placement["planet"] == planet:
            return placement["house"]
    return 10


def _build_advice(tone: str, top_domains: list[str]) -> list[str]:
    advice = list(ADVICE_BY_TONE.get(tone, ["Stay observant.", "Move deliberately."]))

    if "money_finance" in top_domains:
        advice.append("Keep spending deliberate and documented.")
    if "relationships" in top_domains:
        advice.append("Be explicit about expectations in key conversations.")
    if "career_work" in top_domains:
        advice.append("Prioritize the few commitments that materially move work forward.")

    return advice[:3]


def _combined_effect(planet: str, house: int, tone: str, driver) -> str:
    planet_terms = ", ".join(PLANET_MEANINGS[planet][:2])
    house_terms = ", ".join(HOUSE_MEANINGS[house][:2])
    sign_clause = f" in {driver.sign}" if driver and driver.sign else ""
    event_clause = f" during this {driver.event_type}" if driver else ""
    return (
        f"{planet}{sign_clause} themes around {planet_terms} concentrate through house {house} matters like "
        f"{house_terms}{event_clause}, creating a {tone} period."
    )


def _dominant_driver(drivers) -> object | None:
    if not drivers:
        return None
    return max(drivers, key=lambda driver: (driver.intensity, driver.date.toordinal()))


def _tone_for_driver(driver) -> str:
    if driver is None:
        return "mixed"
    if driver.event_type == "eclipse":
        return "volatile"
    if driver.event_type == "station" and driver.motion == "retrograde":
        return "reflective" if driver.planet in {"Mercury", "Venus"} else "serious"
    return TONE_BY_PLANET.get(driver.planet, "mixed")


def _confidence_score(period: PeriodWindow) -> float:
    base = 0.7
    strongest_driver = max((driver.intensity for driver in period.drivers), default=1)
    driver_bonus = min(0.16, strongest_driver * 0.03)
    duration_penalty = 0.0 if period.duration_days <= 45 else 0.04
    return max(0.55, base + driver_bonus - duration_penalty)
