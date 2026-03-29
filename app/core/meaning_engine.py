from __future__ import annotations

from statistics import mean

from app.core.config import (
    ADVICE_BY_TONE,
    DOMAINS,
    DOMAIN_EMOJIS,
    DOMAIN_LABELS,
    EVENT_SCORE_MULTIPLIERS,
    EVENT_TYPE_EXPLANATIONS,
    HOUSE_DOMAIN_MAP,
    HOUSE_EXPLANATIONS,
    HOUSE_MEANINGS,
    PLANET_DOMAIN_BOOSTS,
    PLANET_EXPLANATIONS,
    PLANET_MEANINGS,
    SIGNAL_UI,
    SIGN_EXPLANATIONS,
    TONE_BY_PLANET,
    TONE_UI,
)
from app.core.period_engine import PeriodWindow

CAUTION_TONES = {"stressful", "serious", "volatile", "reflective"}
SUPPORT_TONES = {"constructive", "supportive", "expansive"}
LEVEL_ORDER = {"low": 0, "medium": 1, "high": 2}
SIGNAL_ORDER = ["decision_timing", "politics", "relationships", "money", "health", "travel", "work"]
SIGNAL_PRIORITY = {"decision_timing": 0, "politics": 2, "relationships": 2, "money": 2, "health": 2, "travel": 1, "work": 1}


def build_period_meanings(periods: list[PeriodWindow], natal_chart: dict) -> list[dict]:
    payload: list[dict] = []

    for period in periods:
        driver_contexts = _candidate_driver_contexts(period, natal_chart)
        dominant_drivers = _select_dominant_drivers(driver_contexts)
        tone = _tone_for_drivers(dominant_drivers)
        scores = _score_domains(dominant_drivers, tone)
        top_domains = sorted(scores, key=scores.get, reverse=True)[:3]
        signals = _build_signals(dominant_drivers, tone, scores)
        surfaced_signals = _surface_signals(signals)
        suppressed_signals = [key for key in SIGNAL_ORDER if key not in {item["key"] for item in surfaced_signals}]
        confidence_breakdown = _confidence_breakdown(period, dominant_drivers, top_domains, surfaced_signals, natal_chart)
        guidance = [f"{signal['emoji']} {signal['short_text']}" for signal in surfaced_signals[:4]]
        use_for = _build_use_for(top_domains, tone, signals, surfaced_signals)
        careful_with = _build_careful_with(top_domains, tone, surfaced_signals)
        advice = _build_advice(tone, top_domains, surfaced_signals)

        payload.append(
            {
                "id": period.id,
                "start_date": period.start_date.isoformat(),
                "end_date": period.end_date.isoformat(),
                "tone": tone,
                "domains": scores,
                "advice": advice,
                "drivers": dominant_drivers,
                "dominant_drivers": dominant_drivers,
                "top_domains": top_domains,
                "driver_summary": dominant_drivers[0]["summary"],
                "signals": signals,
                "surfaced_signals": surfaced_signals,
                "suppressed_signals": suppressed_signals,
                "period_guidance": guidance,
                "use_for": use_for,
                "careful_with": careful_with,
                "confidence": confidence_breakdown["overall"],
                "confidence_breakdown": confidence_breakdown,
                "dominant_risk": _dominant_risk(signals),
                "explanation_blocks": _build_explanation_blocks(dominant_drivers),
            }
        )

    return payload


def _candidate_driver_contexts(period: PeriodWindow, natal_chart: dict) -> list[dict]:
    if not period.drivers:
        return [_fallback_driver_context(natal_chart)]

    house_counts: dict[int, int] = {}
    for driver in period.drivers:
        if driver.house is not None:
            house_counts[driver.house] = house_counts.get(driver.house, 0) + 1

    contexts: list[dict] = []
    for driver in period.drivers:
        house = driver.house if driver.house is not None else _house_for_planet(natal_chart, driver.planet)
        sign = driver.sign or _sign_for_planet(natal_chart, driver.planet)
        repeat_bonus = 0.35 if house_counts.get(house, 0) > 1 else 0.0
        weight = _driver_weight(driver.event_type, driver.intensity, driver.planet, house, driver.motion, repeat_bonus)

        contexts.append(
            {
                "planet": driver.planet,
                "house": house,
                "sign": sign,
                "event_type": driver.event_type,
                "motion": driver.motion,
                "summary": _driver_summary(driver.planet, sign, house, driver.event_type, driver.motion),
                "event_text": _event_text(driver.event_type, driver.motion),
                "planet_text": PLANET_EXPLANATIONS[driver.planet],
                "sign_text": SIGN_EXPLANATIONS.get(sign, "The sign adds its own style to how this period expresses itself."),
                "house_text": HOUSE_EXPLANATIONS[house],
                "planet_meaning": ", ".join(PLANET_MEANINGS[driver.planet][:2]),
                "house_meaning": ", ".join(HOUSE_MEANINGS[house][:2]),
                "combined_effect": _combined_effect(driver.planet, sign, house, driver.event_type, driver.motion),
                "weight": round(weight, 2),
            }
        )

    return sorted(contexts, key=lambda item: (item["weight"], item["event_type"] == "eclipse"), reverse=True)


def _fallback_driver_context(natal_chart: dict) -> dict:
    placements = natal_chart.get("placements", [])
    placement = next((item for item in placements if item["planet"] == "Moon"), placements[0] if placements else None)
    planet = placement["planet"] if placement else "Moon"
    house = int(placement["house"]) if placement else 1
    sign = placement["sign"] if placement else "Cancer"

    return {
        "planet": planet,
        "house": house,
        "sign": sign,
        "event_type": "fallback",
        "motion": None,
        "summary": "No single transit dominates this stretch, so the reading leans on the quieter background pattern.",
        "event_text": EVENT_TYPE_EXPLANATIONS["fallback"],
        "planet_text": PLANET_EXPLANATIONS[planet],
        "sign_text": SIGN_EXPLANATIONS.get(sign, "The sign adds its own style to how this period expresses itself."),
        "house_text": HOUSE_EXPLANATIONS[house],
        "planet_meaning": ", ".join(PLANET_MEANINGS[planet][:2]),
        "house_meaning": ", ".join(HOUSE_MEANINGS[house][:2]),
        "combined_effect": _combined_effect(planet, sign, house, "fallback", None),
        "weight": 1.4,
    }


def _select_dominant_drivers(drivers: list[dict]) -> list[dict]:
    if len(drivers) <= 1:
        return drivers

    selected = [drivers[0]]
    strongest_weight = drivers[0]["weight"]

    for candidate in drivers[1:]:
        if len(selected) == 2:
            break
        if candidate["weight"] >= strongest_weight * 0.72 and candidate["house"] != selected[0]["house"]:
            selected.append(candidate)
            continue
        if candidate["event_type"] == "eclipse" and candidate["weight"] >= strongest_weight * 0.62:
            selected.append(candidate)

    return selected


def _score_domains(drivers: list[dict], tone: str) -> dict[str, int]:
    scores = {domain: 2.0 for domain in DOMAINS}
    domain_hits = {domain: 0 for domain in DOMAINS}

    for driver in drivers:
        house_bonus = 1.5 + (driver["weight"] * 0.32)
        planet_bonus = 0.8 + (driver["weight"] * 0.16)

        for domain in HOUSE_DOMAIN_MAP.get(driver["house"], []):
            scores[domain] += house_bonus
            domain_hits[domain] += 1

        for domain in PLANET_DOMAIN_BOOSTS.get(driver["planet"], []):
            scores[domain] += planet_bonus
            domain_hits[domain] += 1

        if driver["event_type"] == "eclipse":
            for domain in HOUSE_DOMAIN_MAP.get(driver["house"], []):
                scores[domain] += 0.8
        if driver["event_type"] == "station" and driver["motion"] == "retrograde":
            scores["study_growth"] += 0.6

    for domain, hits in domain_hits.items():
        if hits >= 2:
            scores[domain] += 0.8

    if tone in CAUTION_TONES:
        scores["health_emotional"] += 0.8
    if tone in {"stressful", "serious"}:
        scores["career_work"] += 0.8
    if tone in SUPPORT_TONES:
        scores["study_growth"] += 0.7
    if tone == "supportive":
        scores["relationships"] += 0.8

    return {domain: max(1, min(10, round(value))) for domain, value in scores.items()}


def _build_signals(drivers: list[dict], tone: str, scores: dict[str, int]) -> dict:
    decision_timing = _decision_signal(drivers, tone)
    politics = _politics_signal(drivers, tone)
    relationships = _relationship_signal(drivers, tone, scores)
    money = _money_signal(drivers, tone, scores)
    health = _health_signal(drivers, tone, scores)
    travel = _travel_signal(drivers, tone, scores)
    work = _work_signal(drivers, tone, scores)

    return {
        "decision_timing": decision_timing,
        "politics": politics,
        "relationships": relationships,
        "money": money,
        "health": health,
        "travel": travel,
        "work": work,
    }


def _decision_signal(drivers: list[dict], tone: str) -> dict:
    caution_score = 0.0
    support_score = 0.0

    for driver in drivers:
        if driver["event_type"] == "eclipse":
            caution_score += 2.0
        if driver["event_type"] == "station" and driver["motion"] == "retrograde":
            caution_score += 1.2
        if driver["planet"] in {"Rahu", "Ketu"}:
            caution_score += 0.9
        if driver["house"] in {8, 12}:
            caution_score += 0.8
        if driver["planet"] in {"Mars", "Saturn"} and driver["house"] in {6, 8, 12}:
            caution_score += 0.6

        if driver["planet"] in {"Sun", "Jupiter", "Venus"} and driver["event_type"] != "eclipse":
            support_score += 1.0
        if driver["house"] in {5, 9, 10, 11} and driver["planet"] in {"Sun", "Jupiter", "Venus", "Mercury"}:
            support_score += 0.5

    status = "mixed"
    short_text = "Decision timing is mixed"
    detail_text = "If something matters, give it a second pass before locking it in."

    if caution_score >= 2.2 or (caution_score >= 1.4 and support_score <= 0.5):
        status = "caution"
        short_text = "Use extra care with big decisions"
        detail_text = "This window looks more emotionally charged or less clear for irreversible choices, promises, or rushed commitments."
    elif support_score >= 1.8 and caution_score <= 0.6 and tone in SUPPORT_TONES:
        status = "good"
        short_text = "A steadier window for key decisions"
        detail_text = "This window looks cleaner for important choices, agreements, and forward movement than the rougher periods around it."

    return {
        "key": "decision_timing",
        "status": status,
        "level": "high" if status != "mixed" else "low",
        "emoji": SIGNAL_UI["decision_timing"]["emoji"],
        "label": SIGNAL_UI["decision_timing"]["label"],
        "short_text": short_text,
        "detail_text": detail_text,
    }


def _politics_signal(drivers: list[dict], tone: str) -> dict:
    high = any(driver["house"] in {7, 8, 11, 12} and driver["planet"] in {"Mars", "Saturn", "Rahu"} for driver in drivers)
    medium = any(driver["house"] in {7, 11, 12} or driver["planet"] in {"Saturn", "Rahu", "Ketu"} for driver in drivers)

    level = "low"
    short_text = "People dynamics look manageable"
    detail_text = "People issues do not look like the main pressure point here."

    if high or (tone in {"stressful", "volatile", "serious"} and medium):
        level = "high"
        short_text = "Watch people and politics more closely"
        detail_text = "This window can bring more mixed motives, hidden agendas, social friction, or office politics than usual."
    elif medium:
        level = "medium"
        short_text = "Keep boundaries clear with people"
        detail_text = "Read the room carefully, avoid oversharing, and make sure expectations are explicit."

    return _signal_payload("politics", level, short_text, detail_text)


def _relationship_signal(drivers: list[dict], tone: str, scores: dict[str, int]) -> dict:
    relationship_house = any(driver["house"] in {5, 7, 8} for driver in drivers)
    level = "low"
    short_text = "Relationships look manageable"
    detail_text = "Relationships are not the sharpest caution area in this window."

    if (scores["relationships"] >= 7 and tone in CAUTION_TONES) or relationship_house and tone in {"volatile", "reflective", "stressful"}:
        level = "high"
        short_text = "Handle relationships with extra care"
        detail_text = "Trust, closeness, expectations, or emotional reactions may feel more delicate than usual."
    elif scores["relationships"] >= 6 or relationship_house:
        level = "medium"
        short_text = "Use a softer touch in relationships"
        detail_text = "This is a good time to clarify tone, expectations, and what each person is actually asking for."

    return _signal_payload("relationships", level, short_text, detail_text)


def _money_signal(drivers: list[dict], tone: str, scores: dict[str, int]) -> dict:
    money_house = any(driver["house"] in {2, 8, 11} for driver in drivers)
    level = "low"
    short_text = "Money pressure looks manageable"
    detail_text = "Finances are not the sharpest caution area in this window."

    if (scores["money_finance"] >= 7 and tone in {"stressful", "volatile", "serious"}) or (money_house and any(driver["house"] == 8 for driver in drivers)):
        level = "high"
        short_text = "Keep money decisions measured"
        detail_text = "Use extra care with spending, borrowing, shared finances, debt, or rushed financial commitments."
    elif scores["money_finance"] >= 6 or money_house:
        level = "medium"
        short_text = "Double-check financial choices"
        detail_text = "Review numbers, payment timing, and the real cost before agreeing to anything."

    return _signal_payload("money", level, short_text, detail_text)


def _health_signal(drivers: list[dict], tone: str, scores: dict[str, int]) -> dict:
    health_house = any(driver["house"] in {1, 6, 8, 12} for driver in drivers)
    level = "low"
    short_text = "Health pressure looks manageable"
    detail_text = "Health is not the main caution area in this window."

    if (scores["health_emotional"] >= 7 and tone in CAUTION_TONES) or (health_house and tone in CAUTION_TONES):
        level = "high"
        short_text = "Mind energy, stress, and health"
        detail_text = "Protect sleep, energy, stress levels, and follow through on early warning signs instead of pushing through them."
    elif scores["health_emotional"] >= 6 or health_house:
        level = "medium"
        short_text = "Take better care of your routine"
        detail_text = "Routine, pacing, hydration, rest, and nervous-system load matter more than usual here."

    return _signal_payload("health", level, short_text, detail_text)


def _travel_signal(drivers: list[dict], tone: str, scores: dict[str, int]) -> dict:
    travel_house = any(driver["house"] in {3, 9, 12} for driver in drivers)
    level = "low"
    short_text = "Travel themes stay in the background"
    detail_text = "Travel, movement, or distance are not central here."

    if scores["travel_overseas"] >= 7 or any(driver["planet"] in {"Jupiter", "Rahu"} and travel_house for driver in drivers):
        level = "medium" if tone in CAUTION_TONES else "high"
        short_text = "Travel or movement becomes more important"
        detail_text = "Movement, distance, paperwork, or a wider horizon may matter more than usual in this period."
        if tone in CAUTION_TONES:
            short_text = "Plan travel and movement carefully"
            detail_text = "Travel or movement may be meaningful here, but build in margin for timing, logistics, and fatigue."

    return _signal_payload("travel", level, short_text, detail_text)


def _work_signal(drivers: list[dict], tone: str, scores: dict[str, int]) -> dict:
    work_house = any(driver["house"] in {6, 10, 11} for driver in drivers)
    level = "low"
    short_text = "Work pressure looks manageable"
    detail_text = "Work is present but not the sharpest pressure point here."

    if (scores["career_work"] >= 7 and tone in {"stressful", "serious"}) or any(driver["planet"] in {"Saturn", "Mars"} and work_house for driver in drivers):
        level = "high"
        short_text = "Expect more work pressure or responsibility"
        detail_text = "This period can demand more discipline, accountability, deadlines, or selective prioritization."
    elif scores["career_work"] >= 6 or work_house:
        level = "medium"
        short_text = "Work deserves steady attention"
        detail_text = "Work matters here, but it responds better to structure and consistency than to rushing."

    return _signal_payload("work", level, short_text, detail_text)


def _surface_signals(signals: dict) -> list[dict]:
    surfaced = []

    for key in SIGNAL_ORDER:
        signal = signals[key]
        if key == "decision_timing":
            if signal["status"] != "mixed":
                surfaced.append(signal)
            continue
        if signal["level"] in {"medium", "high"}:
            surfaced.append(signal)

    surfaced.sort(key=lambda item: (_signal_strength(item), SIGNAL_PRIORITY.get(item["key"], 0)), reverse=True)
    return surfaced


def _build_use_for(top_domains: list[str], tone: str, signals: dict, surfaced_signals: list[dict]) -> list[str]:
    items: list[str] = []

    if signals["decision_timing"]["status"] == "good":
        items.append("making clearer decisions and moving important plans forward")

    domain_use_map = {
        "career_work": "steady work progress and visible responsibilities",
        "money_finance": "measured financial planning and sorting practical priorities",
        "relationships": "honest conversations and strengthening key ties",
        "health_emotional": "resetting routines and listening to what your body or mood is telling you",
        "travel_overseas": "travel planning, learning, and looking at the bigger picture",
        "study_growth": "study, strategy, personal growth, and long-range planning",
    }

    for domain in top_domains:
        phrase = domain_use_map[domain]
        if phrase not in items and not (domain == "money_finance" and signals["money"]["level"] == "high"):
            items.append(phrase)
        if len(items) == 3:
            break

    if not items and tone in SUPPORT_TONES:
        items.append("using the steadier tone of this period to move one or two priorities forward")
    elif not items:
        items.append("slower review, cleanup, and making fewer but better-timed moves")

    return items[:3]


def _build_careful_with(top_domains: list[str], tone: str, surfaced_signals: list[dict]) -> list[str]:
    items: list[str] = []
    caution_map = {
        "decision_timing": "rushed decisions, big promises, and irreversible commitments",
        "politics": "oversharing, office politics, or trusting unclear motives too quickly",
        "relationships": "sensitive conversations, assumptions, and emotional overreactions",
        "money": "risky spending, debt, or vague money agreements",
        "health": "pushing through fatigue, stress, or ignored warning signs",
        "travel": "tight travel timing, paperwork, or overpacked schedules",
        "work": "taking on too much responsibility without enough margin",
    }

    for signal in surfaced_signals:
        if signal["key"] == "decision_timing" and signal["status"] != "caution":
            continue
        caution = caution_map.get(signal["key"])
        if caution and caution not in items:
            items.append(caution)

    if not items and tone in CAUTION_TONES:
        items.append("overloading your schedule or reacting too quickly")
    if not items and "money_finance" in top_domains:
        items.append("treating financial choices as small when they deserve a closer look")

    return items[:3]


def _build_advice(tone: str, top_domains: list[str], surfaced_signals: list[dict]) -> list[str]:
    advice = list(ADVICE_BY_TONE.get(tone, ["Stay observant.", "Move deliberately."]))

    signal_index = {signal["key"]: signal for signal in surfaced_signals}

    if signal_index.get("decision_timing", {}).get("status") == "caution":
        advice.insert(0, "Delay major decisions if the choice can wait.")
    if signal_index.get("politics", {}).get("level") == "high":
        advice.append("Keep plans tighter and confirm who really needs to know what.")
    if signal_index.get("money", {}).get("level") == "high":
        advice.append("Write numbers down and avoid vague financial promises.")
    if signal_index.get("health", {}).get("level") == "high":
        advice.append("Protect sleep, routine, and recovery before performance slips.")
    if "relationships" in top_domains:
        advice.append("Say the awkward thing clearly instead of letting assumptions grow.")
    if "career_work" in top_domains:
        advice.append("Choose the few responsibilities that actually move work forward.")

    seen: set[str] = set()
    deduped: list[str] = []
    for item in advice:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)

    return deduped[:3]


def _build_explanation_blocks(drivers: list[dict]) -> list[dict]:
    blocks: list[dict] = []

    for driver in drivers:
        title = _driver_title(driver)
        items = [driver["event_text"], driver["planet_text"], driver["sign_text"], driver["house_text"]]
        blocks.append(
            {
                "title": title,
                "summary": driver["combined_effect"],
                "items": items,
            }
        )

    return blocks


def _confidence_breakdown(
    period: PeriodWindow,
    dominant_drivers: list[dict],
    top_domains: list[str],
    surfaced_signals: list[dict],
    natal_chart: dict,
) -> dict:
    driver_strength = min(0.93, 0.56 + (mean(driver["weight"] for driver in dominant_drivers) * 0.05))
    signal_agreement = _signal_agreement(dominant_drivers, top_domains, surfaced_signals)
    data_quality = _data_quality_score(natal_chart)

    overall = max(0.54, min(0.92, (driver_strength * 0.45) + (signal_agreement * 0.25) + (data_quality * 0.30)))
    if period.duration_days > 50:
        overall -= 0.03

    overall = round(max(0.54, overall), 2)

    if overall >= 0.82:
        label = "High"
    elif overall >= 0.70:
        label = "Medium"
    else:
        label = "Cautious"

    return {
        "overall": overall,
        "label": label,
        "event_strength": round(driver_strength, 2),
        "signal_agreement": round(signal_agreement, 2),
        "data_quality": round(data_quality, 2),
    }


def _signal_agreement(dominant_drivers: list[dict], top_domains: list[str], surfaced_signals: list[dict]) -> float:
    matching_domains = 0
    for driver in dominant_drivers:
        if any(domain in top_domains for domain in HOUSE_DOMAIN_MAP.get(driver["house"], [])):
            matching_domains += 1

    domain_alignment = matching_domains / max(1, len(dominant_drivers))
    signal_bonus = min(0.2, len(surfaced_signals) * 0.04)
    return min(0.9, 0.62 + (domain_alignment * 0.14) + signal_bonus)


def _data_quality_score(natal_chart: dict) -> float:
    source = natal_chart.get("location", {}).get("source", "")
    backend = natal_chart.get("ephemeris_backend", "")

    score = 0.72
    if "manual_coordinates" in source:
        score += 0.08
    else:
        score -= 0.02
    if "manual_timezone" in source:
        score += 0.04
    if backend == "moshier_fallback":
        score -= 0.08
    if natal_chart.get("warnings"):
        score -= 0.02

    return max(0.56, min(0.9, score))


def _dominant_risk(signals: dict) -> dict:
    caution_signals = [
        signal
        for key, signal in signals.items()
        if key != "decision_timing" and signal["level"] in {"medium", "high"}
    ]
    if caution_signals:
        return max(caution_signals, key=lambda item: LEVEL_ORDER[item["level"]])
    return signals["decision_timing"]


def _signal_payload(key: str, level: str, short_text: str, detail_text: str) -> dict:
    return {
        "key": key,
        "level": level,
        "emoji": SIGNAL_UI[key]["emoji"],
        "label": SIGNAL_UI[key]["label"],
        "short_text": short_text,
        "detail_text": detail_text,
    }


def _signal_strength(signal: dict) -> int:
    if signal["key"] == "decision_timing":
        return 1 if signal["status"] != "mixed" else 0
    return LEVEL_ORDER[signal["level"]]


def _house_for_planet(natal_chart: dict, planet: str) -> int:
    for placement in natal_chart.get("placements", []):
        if placement["planet"] == planet:
            return int(placement["house"])
    return 10


def _sign_for_planet(natal_chart: dict, planet: str) -> str:
    for placement in natal_chart.get("placements", []):
        if placement["planet"] == planet:
            return placement["sign"]
    return "Leo"


def _driver_weight(event_type: str, intensity: int, planet: str, house: int, motion: str | None, repeat_bonus: float) -> float:
    weight = intensity * EVENT_SCORE_MULTIPLIERS.get(event_type, 1.0)

    if event_type == "station" and motion == "retrograde":
        weight += 0.8
    if planet in {"Saturn", "Jupiter", "Rahu", "Ketu"}:
        weight += 0.35
    if house in {1, 4, 7, 10}:
        weight += 0.2
    if house in {6, 8, 12} and event_type in {"station", "eclipse"}:
        weight += 0.4

    return weight + repeat_bonus


def _tone_for_drivers(drivers: list[dict]) -> str:
    positive = 0.0
    caution = 0.0

    for driver in drivers:
        if driver["event_type"] == "eclipse":
            caution += 2.2
        if driver["event_type"] == "station" and driver["motion"] == "retrograde":
            caution += 1.5

        if driver["planet"] in {"Mars", "Saturn", "Rahu", "Ketu"}:
            caution += 1.0
        if driver["planet"] in {"Sun", "Jupiter", "Venus"}:
            positive += 1.0
        if driver["house"] in {6, 8, 12}:
            caution += 0.7
        if driver["house"] in {5, 9, 10, 11}:
            positive += 0.5

    if caution >= positive + 1.7:
        if any(driver["event_type"] == "eclipse" or driver["planet"] == "Rahu" for driver in drivers):
            return "volatile"
        if any(driver["planet"] == "Mars" for driver in drivers):
            return "stressful"
        if any(driver["planet"] in {"Saturn", "Ketu"} for driver in drivers):
            return "serious" if any(driver["planet"] == "Saturn" for driver in drivers) else "reflective"
        return "mixed"

    if positive >= caution + 1.5:
        if any(driver["planet"] == "Jupiter" for driver in drivers):
            return "expansive"
        if any(driver["planet"] == "Venus" for driver in drivers):
            return "supportive"
        if any(driver["planet"] == "Mercury" for driver in drivers):
            return "active"
        return "constructive"

    if any(driver["planet"] == "Mercury" for driver in drivers):
        return "active"
    return TONE_BY_PLANET.get(drivers[0]["planet"], "mixed")


def _driver_title(driver: dict) -> str:
    event_label = {
        "eclipse": _eclipse_name(driver["planet"]),
        "station": "station",
        "ingress": "sign change",
        "fallback": "background pattern",
    }[driver["event_type"]]

    if driver["event_type"] == "fallback":
        return f"{driver['planet']} background pattern"
    if driver["event_type"] == "eclipse":
        return f"{event_label} in {driver['sign']} / House {driver['house']}"
    return f"{driver['planet']} {event_label} in {driver['sign']} / House {driver['house']}"


def _driver_summary(planet: str, sign: str, house: int, event_type: str, motion: str | None) -> str:
    if event_type == "eclipse":
        return f"{_eclipse_name(planet)} themes put extra weight on {HOUSE_MEANINGS[house][0]} matters in {sign} style."
    if event_type == "station" and motion == "retrograde":
        return f"{planet} retrograde slows things down and makes house {house} themes harder to ignore."
    if event_type == "station":
        return f"{planet} stations and makes house {house} themes louder for a while."
    if event_type == "ingress":
        return f"{planet} shifts into {sign}, so house {house} topics start taking more of your attention."
    return "No single transit dominates this stretch, so the reading leans on the background pattern."


def _event_text(event_type: str, motion: str | None) -> str:
    if event_type == "station" and motion == "retrograde":
        return "A retrograde station slows a planet down and often makes review, delay, and repetition more obvious."
    if event_type == "station" and motion == "direct":
        return "A direct station tends to unstick a theme that was stalled, slow, or under review."
    return EVENT_TYPE_EXPLANATIONS[event_type]


def _combined_effect(planet: str, sign: str, house: int, event_type: str, motion: str | None) -> str:
    sign_clause = SIGN_EXPLANATIONS[sign]
    house_clause = HOUSE_EXPLANATIONS[house]

    if event_type == "eclipse":
        return f"{planet} themes feel louder and more exposed here. {sign_clause} {house_clause}"
    if event_type == "station" and motion == "retrograde":
        return f"{planet} themes slow down for review here. {sign_clause} {house_clause}"
    if event_type == "station":
        return f"{planet} themes become more noticeable here. {sign_clause} {house_clause}"
    if event_type == "ingress":
        return f"{planet} starts working through a new area here. {sign_clause} {house_clause}"
    return f"This is a quieter stretch. {sign_clause} {house_clause}"


def _eclipse_name(planet: str) -> str:
    return "Lunar eclipse" if planet == "Moon" else "Solar eclipse"
