from __future__ import annotations

from app.core.config import (
    ADVICE_BY_TONE,
    DOMAINS,
    HOUSE_DOMAIN_MAP,
    HOUSE_MEANINGS,
    PLANET_MEANINGS,
    SIGNAL_UI,
    TONE_UI,
    TONE_BY_PLANET,
)
from app.core.period_engine import PeriodWindow

CAUTION_TONES = {"stressful", "serious", "volatile", "reflective"}
SUPPORT_TONES = {"constructive", "supportive", "expansive"}
LEVEL_ORDER = {"low": 0, "medium": 1, "high": 2}


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
        signals = _build_master_signals(period, planet, house, tone, scores, driver)
        advice = _build_advice(tone, top_domains, signals)
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
                "signals": signals,
                "period_guidance": _build_period_guidance(signals),
                "confidence": round(_confidence_score(period), 2),
            }
        )

    return payload


def _house_for_planet(natal_chart: dict, planet: str) -> int:
    for placement in natal_chart.get("placements", []):
        if placement["planet"] == planet:
            return placement["house"]
    return 10


def _build_advice(tone: str, top_domains: list[str], signals: dict) -> list[str]:
    advice = list(ADVICE_BY_TONE.get(tone, ["Stay observant.", "Move deliberately."]))

    if "money_finance" in top_domains:
        advice.append("Keep spending deliberate and documented.")
    if "relationships" in top_domains:
        advice.append("Be explicit about expectations in key conversations.")
    if "career_work" in top_domains:
        advice.append("Prioritize the few commitments that materially move work forward.")
    if signals["decision_timing"]["status"] == "caution":
        advice.insert(0, "Delay major decisions if the choice can wait.")
    if signals["backstabbers"]["level"] == "high":
        advice.append("Keep plans tight and be careful who you trust.")
    if signals["health"]["level"] == "high":
        advice.append("Prioritize rest, routine, and early check-ins on symptoms.")

    return advice[:3]


def _combined_effect(planet: str, house: int, tone: str, driver) -> str:
    planet_terms = ", ".join(PLANET_MEANINGS[planet][:2])
    house_terms = ", ".join(HOUSE_MEANINGS[house][:2])
    sign_clause = f" in {driver.sign}" if driver and driver.sign else ""
    event_clause = f" during this {driver.event_type}" if driver else ""
    tone_label = TONE_UI[tone]["label"].lower()
    article = "an" if tone_label[:1] in {"a", "e", "i", "o", "u"} else "a"
    return (
        f"{planet}{sign_clause} themes around {planet_terms} concentrate through house {house} matters like "
        f"{house_terms}{event_clause}, creating {article} {tone_label} period."
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


def _build_master_signals(period: PeriodWindow, planet: str, house: int, tone: str, scores: dict, driver) -> dict:
    decision_timing = _decision_signal(planet, house, tone, driver)
    backstabbers = _backstabber_signal(planet, house, tone)
    relationships = _relationship_signal(house, tone, scores)
    money = _money_signal(house, tone, scores)
    health = _health_signal(house, tone, scores)

    return {
        "decision_timing": decision_timing,
        "backstabbers": backstabbers,
        "relationships": relationships,
        "money": money,
        "health": health,
        "dominant_risk": _dominant_risk(backstabbers, relationships, money, health),
        "driver_count": len(period.drivers),
    }


def _decision_signal(planet: str, house: int, tone: str, driver) -> dict:
    status = "mixed"
    short_text = "Decision timing looks mixed"
    detail_text = "If something is important, give it a second pass before locking it in."

    if driver and (
        driver.event_type == "eclipse"
        or (driver.event_type == "station" and driver.motion == "retrograde")
        or tone in CAUTION_TONES
    ):
        status = "caution"
        short_text = "Use extra care with big decisions"
        detail_text = "This looks less clean for major commitments, promises, or irreversible choices."
    elif tone in SUPPORT_TONES and planet in {"Sun", "Jupiter", "Venus"} and house not in {8, 12}:
        status = "good"
        short_text = "A steadier window for key decisions"
        detail_text = "This looks like one of the cleaner windows to make decisions and move plans forward."

    return {
        "key": "decision_timing",
        "status": status,
        "emoji": SIGNAL_UI["decision_timing"]["emoji"],
        "label": SIGNAL_UI["decision_timing"]["label"],
        "short_text": short_text,
        "detail_text": detail_text,
    }


def _backstabber_signal(planet: str, house: int, tone: str) -> dict:
    level = "low"
    short_text = "Politics look manageable"
    detail_text = "People dynamics do not look like the main issue in this period."

    if (house in {7, 8, 11, 12} and planet in {"Mars", "Rahu", "Saturn"}) or (
        tone in {"stressful", "volatile", "serious"} and house in {7, 11, 12}
    ):
        level = "high"
        short_text = "Watch people and politics more closely"
        detail_text = "Keep an eye on hidden agendas, gossip, office politics, or people who may not be fully straightforward."
    elif house in {7, 11, 12} or planet in {"Rahu", "Saturn"}:
        level = "medium"
        short_text = "Be mindful of mixed motives"
        detail_text = "Keep boundaries clear and avoid oversharing sensitive plans."

    return {
        "key": "backstabbers",
        "level": level,
        "emoji": SIGNAL_UI["backstabbers"]["emoji"],
        "label": SIGNAL_UI["backstabbers"]["label"],
        "short_text": short_text,
        "detail_text": detail_text,
    }


def _relationship_signal(house: int, tone: str, scores: dict) -> dict:
    level = "low"
    short_text = "Relationships look manageable"
    detail_text = "Connection matters are not the main pressure point here."

    relationship_score = scores["relationships"]
    if (relationship_score >= 6 and tone in CAUTION_TONES) or house in {5, 7, 8} and tone in {"volatile", "stressful", "reflective"}:
        level = "high"
        short_text = "Handle relationships with extra care"
        detail_text = "This is a more fragile window for romance, trust, arguments, and emotional misunderstandings."
    elif relationship_score >= 5 or house in {5, 7, 11}:
        level = "medium"
        short_text = "Use a softer touch in relationships"
        detail_text = "Clarify expectations and do not rely on assumptions in close relationships."

    return {
        "key": "relationships",
        "level": level,
        "emoji": SIGNAL_UI["relationships"]["emoji"],
        "label": SIGNAL_UI["relationships"]["label"],
        "short_text": short_text,
        "detail_text": detail_text,
    }


def _money_signal(house: int, tone: str, scores: dict) -> dict:
    level = "low"
    short_text = "Money pressure looks manageable"
    detail_text = "Finances are not the sharpest caution area in this period."

    money_score = scores["money_finance"]
    if (money_score >= 6 and tone in {"stressful", "volatile", "serious"}) or house in {2, 8} and tone in CAUTION_TONES:
        level = "high"
        short_text = "Keep money decisions measured"
        detail_text = "Avoid risky spending, loans, rushed purchases, and unclear money commitments."
    elif money_score >= 5 or house in {2, 8, 11}:
        level = "medium"
        short_text = "Double-check financial choices"
        detail_text = "Review budgets, contracts, and payment timing before committing."

    return {
        "key": "money",
        "level": level,
        "emoji": SIGNAL_UI["money"]["emoji"],
        "label": SIGNAL_UI["money"]["label"],
        "short_text": short_text,
        "detail_text": detail_text,
    }


def _health_signal(house: int, tone: str, scores: dict) -> dict:
    level = "low"
    short_text = "Health pressure looks manageable"
    detail_text = "Health is not the strongest caution flag in this window."

    health_score = scores["health_emotional"]
    if (health_score >= 6 and tone in CAUTION_TONES) or house in {1, 6, 8, 12} and tone in CAUTION_TONES:
        level = "high"
        short_text = "Mind energy, stress, and health"
        detail_text = "Protect energy, sleep, stress levels, and do not ignore early warning signs."
    elif health_score >= 5 or house in {1, 6, 12}:
        level = "medium"
        short_text = "Take better care of your routine"
        detail_text = "Keep routines steady and reduce avoidable stress where possible."

    return {
        "key": "health",
        "level": level,
        "emoji": SIGNAL_UI["health"]["emoji"],
        "label": SIGNAL_UI["health"]["label"],
        "short_text": short_text,
        "detail_text": detail_text,
    }


def _dominant_risk(*signals: dict) -> dict:
    ranked = max(signals, key=lambda item: LEVEL_ORDER[item["level"]])
    return ranked


def _build_period_guidance(signals: dict) -> list[str]:
    guidance = [f"{signals['decision_timing']['emoji']} {signals['decision_timing']['short_text']}"]

    for key in ["backstabbers", "relationships", "money", "health"]:
        signal = signals[key]
        if signal["level"] in {"high", "medium"}:
            guidance.append(f"{signal['emoji']} {signal['short_text']}")

    return guidance[:4]


def _confidence_score(period: PeriodWindow) -> float:
    base = 0.7
    strongest_driver = max((driver.intensity for driver in period.drivers), default=1)
    driver_bonus = min(0.16, strongest_driver * 0.03)
    duration_penalty = 0.0 if period.duration_days <= 45 else 0.04
    return max(0.55, base + driver_bonus - duration_penalty)
