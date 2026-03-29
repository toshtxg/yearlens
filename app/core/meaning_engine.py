from __future__ import annotations

from statistics import mean

from app.core.config import (
    DOMAINS,
    DOMAIN_EMOJIS,
    EVENT_SCORE_MULTIPLIERS,
    HOUSE_DOMAIN_MAP,
    PLANET_DOMAIN_BOOSTS,
    TONE_BY_PLANET,
    get_advice_by_tone,
    get_domain_labels,
    get_event_type_explanations,
    get_house_explanations,
    get_house_meanings,
    get_planet_explanations,
    get_signal_ui,
    get_sign_explanations,
    get_planet_meanings,
)
from app.core.meaning_strings import (
    ADVICE_EXTRA,
    CAREFUL_WITH,
    COMBINED_EFFECT,
    DECISION_SIGNAL,
    DRIVER_SUMMARY,
    DRIVER_TITLE,
    ECLIPSE_NAMES,
    EVENT_LABELS,
    EVENT_TEXT,
    FALLBACK_SIGN_TEXT,
    FALLBACK_SUMMARY,
    HEALTH_SIGNAL,
    MONEY_SIGNAL,
    POLITICS_SIGNAL,
    RELATIONSHIP_SIGNAL,
    TRAVEL_SIGNAL,
    USE_FOR,
    WORK_SIGNAL,
)
from app.core.period_engine import PeriodWindow

CAUTION_TONES = {"stressful", "serious", "volatile", "reflective"}
SUPPORT_TONES = {"constructive", "supportive", "expansive"}
LEVEL_ORDER = {"low": 0, "medium": 1, "high": 2}
SIGNAL_ORDER = ["decision_timing", "politics", "relationships", "money", "health", "travel", "work"]
SIGNAL_PRIORITY = {"decision_timing": 3, "politics": 2, "relationships": 2, "money": 2, "health": 2, "travel": 1, "work": 1}


def build_period_meanings(periods: list[PeriodWindow], natal_chart: dict, lang: str = "en") -> list[dict]:
    payload: list[dict] = []

    for period in periods:
        driver_contexts = _candidate_driver_contexts(period, natal_chart, lang)
        dominant_drivers = _select_dominant_drivers(driver_contexts)
        tone = _tone_for_drivers(dominant_drivers)
        scores = _score_domains(dominant_drivers, tone)
        top_domains = sorted(scores, key=scores.get, reverse=True)[:3]
        signals = _build_signals(dominant_drivers, tone, scores, lang)
        surfaced_signals = _surface_signals(signals)
        suppressed_signals = [key for key in SIGNAL_ORDER if key not in {item["key"] for item in surfaced_signals}]
        confidence_breakdown = _confidence_breakdown(period, dominant_drivers, top_domains, surfaced_signals, natal_chart)
        guidance = [f"{signal['emoji']} {signal['short_text']}" for signal in surfaced_signals[:4]]
        use_for = _build_use_for(top_domains, tone, signals, surfaced_signals, lang)
        careful_with = _build_careful_with(top_domains, tone, surfaced_signals, lang)
        advice = _build_advice(tone, top_domains, surfaced_signals, lang)

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


def _candidate_driver_contexts(period: PeriodWindow, natal_chart: dict, lang: str) -> list[dict]:
    if not period.drivers:
        return [_fallback_driver_context(natal_chart, lang)]

    house_counts: dict[int, int] = {}
    for driver in period.drivers:
        if driver.house is not None:
            house_counts[driver.house] = house_counts.get(driver.house, 0) + 1

    planet_explanations = get_planet_explanations(lang)
    sign_explanations = get_sign_explanations(lang)
    house_explanations = get_house_explanations(lang)
    planet_meanings = get_planet_meanings(lang)
    house_meanings = get_house_meanings(lang)

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
                "summary": _driver_summary(driver.planet, sign, house, driver.event_type, driver.motion, lang),
                "event_text": _event_text(driver.event_type, driver.motion, lang),
                "planet_text": planet_explanations[driver.planet],
                "sign_text": sign_explanations.get(sign, FALLBACK_SIGN_TEXT[lang]),
                "house_text": house_explanations[house],
                "planet_meaning": ", ".join(planet_meanings[driver.planet][:2]),
                "house_meaning": ", ".join(house_meanings[house][:2]),
                "combined_effect": _combined_effect(driver.planet, sign, house, driver.event_type, driver.motion, lang),
                "weight": round(weight, 2),
            }
        )

    return sorted(contexts, key=lambda item: (item["weight"], item["event_type"] == "eclipse"), reverse=True)


def _fallback_driver_context(natal_chart: dict, lang: str) -> dict:
    placements = natal_chart.get("placements", [])
    placement = next((item for item in placements if item["planet"] == "Moon"), placements[0] if placements else None)
    planet = placement["planet"] if placement else "Moon"
    house = int(placement["house"]) if placement else 1
    sign = placement["sign"] if placement else "Cancer"

    planet_explanations = get_planet_explanations(lang)
    sign_explanations = get_sign_explanations(lang)
    house_explanations = get_house_explanations(lang)
    planet_meanings = get_planet_meanings(lang)
    house_meanings = get_house_meanings(lang)
    event_type_explanations = get_event_type_explanations(lang)

    return {
        "planet": planet,
        "house": house,
        "sign": sign,
        "event_type": "fallback",
        "motion": None,
        "summary": FALLBACK_SUMMARY[lang],
        "event_text": event_type_explanations["fallback"],
        "planet_text": planet_explanations[planet],
        "sign_text": sign_explanations.get(sign, FALLBACK_SIGN_TEXT[lang]),
        "house_text": house_explanations[house],
        "planet_meaning": ", ".join(planet_meanings[planet][:2]),
        "house_meaning": ", ".join(house_meanings[house][:2]),
        "combined_effect": _combined_effect(planet, sign, house, "fallback", None, lang),
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


def _build_signals(drivers: list[dict], tone: str, scores: dict[str, int], lang: str) -> dict:
    return {
        "decision_timing": _decision_signal(drivers, tone, lang),
        "politics": _politics_signal(drivers, tone, lang),
        "relationships": _relationship_signal(drivers, tone, scores, lang),
        "money": _money_signal(drivers, tone, scores, lang),
        "health": _health_signal(drivers, tone, scores, lang),
        "travel": _travel_signal(drivers, tone, scores, lang),
        "work": _work_signal(drivers, tone, scores, lang),
    }


def _decision_signal(drivers: list[dict], tone: str, lang: str) -> dict:
    texts = DECISION_SIGNAL[lang]
    signal_ui = get_signal_ui(lang)

    caution_driver = any(
        driver["event_type"] == "eclipse"
        or (driver["event_type"] == "station" and driver["motion"] == "retrograde")
        or driver["planet"] in {"Rahu", "Ketu"}
        or driver["house"] in {8, 12}
        for driver in drivers
    )
    support_driver = any(
        driver["planet"] in {"Sun", "Jupiter", "Venus"}
        and driver["event_type"] != "eclipse"
        and driver["house"] not in {8, 12}
        for driver in drivers
    )

    status = "mixed"
    short_text, detail_text = texts["mixed"]

    if caution_driver or tone in CAUTION_TONES:
        status = "caution"
        short_text, detail_text = texts["caution"]
    elif support_driver and tone in SUPPORT_TONES:
        status = "good"
        short_text, detail_text = texts["good"]

    return {
        "key": "decision_timing",
        "status": status,
        "level": "high" if status != "mixed" else "low",
        "emoji": signal_ui["decision_timing"]["emoji"],
        "label": signal_ui["decision_timing"]["label"],
        "short_text": short_text,
        "detail_text": detail_text,
    }


def _politics_signal(drivers: list[dict], tone: str, lang: str) -> dict:
    texts = POLITICS_SIGNAL[lang]
    high = any(driver["house"] in {7, 8, 11, 12} and driver["planet"] in {"Mars", "Saturn", "Rahu"} for driver in drivers)
    medium = any(driver["house"] in {7, 11, 12} or driver["planet"] in {"Saturn", "Rahu", "Ketu"} for driver in drivers)

    level = "low"
    short_text, detail_text = texts["low"]

    if high or (tone in {"stressful", "volatile", "serious"} and medium):
        level = "high"
        short_text, detail_text = texts["high"]
    elif medium:
        level = "medium"
        short_text, detail_text = texts["medium"]

    return _signal_payload("politics", level, short_text, detail_text, lang)


def _relationship_signal(drivers: list[dict], tone: str, scores: dict[str, int], lang: str) -> dict:
    texts = RELATIONSHIP_SIGNAL[lang]
    relationship_house = any(driver["house"] in {5, 7, 8} for driver in drivers)
    level = "low"
    short_text, detail_text = texts["low"]

    if (scores["relationships"] >= 7 and tone in CAUTION_TONES) or relationship_house and tone in {"volatile", "reflective", "stressful"}:
        level = "high"
        short_text, detail_text = texts["high"]
    elif scores["relationships"] >= 6 or relationship_house:
        level = "medium"
        short_text, detail_text = texts["medium"]

    return _signal_payload("relationships", level, short_text, detail_text, lang)


def _money_signal(drivers: list[dict], tone: str, scores: dict[str, int], lang: str) -> dict:
    texts = MONEY_SIGNAL[lang]
    money_house = any(driver["house"] in {2, 8, 11} for driver in drivers)
    level = "low"
    short_text, detail_text = texts["low"]

    if (scores["money_finance"] >= 7 and tone in {"stressful", "volatile", "serious"}) or (money_house and any(driver["house"] == 8 for driver in drivers)):
        level = "high"
        short_text, detail_text = texts["high"]
    elif scores["money_finance"] >= 6 or money_house:
        level = "medium"
        short_text, detail_text = texts["medium"]

    return _signal_payload("money", level, short_text, detail_text, lang)


def _health_signal(drivers: list[dict], tone: str, scores: dict[str, int], lang: str) -> dict:
    texts = HEALTH_SIGNAL[lang]
    health_house = any(driver["house"] in {1, 6, 8, 12} for driver in drivers)
    level = "low"
    short_text, detail_text = texts["low"]

    if (scores["health_emotional"] >= 7 and tone in CAUTION_TONES) or (health_house and tone in CAUTION_TONES):
        level = "high"
        short_text, detail_text = texts["high"]
    elif scores["health_emotional"] >= 6 or health_house:
        level = "medium"
        short_text, detail_text = texts["medium"]

    return _signal_payload("health", level, short_text, detail_text, lang)


def _travel_signal(drivers: list[dict], tone: str, scores: dict[str, int], lang: str) -> dict:
    texts = TRAVEL_SIGNAL[lang]
    travel_house = any(driver["house"] in {3, 9, 12} for driver in drivers)
    level = "low"
    short_text, detail_text = texts["low"]

    if scores["travel_overseas"] >= 7 or any(driver["planet"] in {"Jupiter", "Rahu"} and travel_house for driver in drivers):
        level = "medium" if tone in CAUTION_TONES else "high"
        short_text, detail_text = texts["high"]
        if tone in CAUTION_TONES:
            short_text, detail_text = texts["caution"]

    return _signal_payload("travel", level, short_text, detail_text, lang)


def _work_signal(drivers: list[dict], tone: str, scores: dict[str, int], lang: str) -> dict:
    texts = WORK_SIGNAL[lang]
    work_house = any(driver["house"] in {6, 10, 11} for driver in drivers)
    level = "low"
    short_text, detail_text = texts["low"]

    if (scores["career_work"] >= 7 and tone in {"stressful", "serious"}) or any(driver["planet"] in {"Saturn", "Mars"} and work_house for driver in drivers):
        level = "high"
        short_text, detail_text = texts["high"]
    elif scores["career_work"] >= 6 or work_house:
        level = "medium"
        short_text, detail_text = texts["medium"]

    return _signal_payload("work", level, short_text, detail_text, lang)


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


def _build_use_for(top_domains: list[str], tone: str, signals: dict, surfaced_signals: list[dict], lang: str) -> list[str]:
    items: list[str] = []
    texts = USE_FOR[lang]

    if signals["decision_timing"]["status"] == "good":
        items.append(texts["good_decisions"])

    for domain in top_domains:
        phrase = texts[domain]
        if phrase not in items and not (domain == "money_finance" and signals["money"]["level"] == "high"):
            items.append(phrase)
        if len(items) == 3:
            break

    if not items and tone in SUPPORT_TONES:
        items.append(texts["support_fallback"])
    elif not items:
        items.append(texts["caution_fallback"])

    return items[:3]


def _build_careful_with(top_domains: list[str], tone: str, surfaced_signals: list[dict], lang: str) -> list[str]:
    items: list[str] = []
    texts = CAREFUL_WITH[lang]

    for signal in surfaced_signals:
        if signal["key"] == "decision_timing" and signal["status"] != "caution":
            continue
        caution = texts.get(signal["key"])
        if caution and caution not in items:
            items.append(caution)

    if not items and tone in CAUTION_TONES:
        items.append(texts["caution_fallback"])
    if not items and "money_finance" in top_domains:
        items.append(texts["money_fallback"])

    return items[:3]


def _build_advice(tone: str, top_domains: list[str], surfaced_signals: list[dict], lang: str) -> list[str]:
    advice_by_tone = get_advice_by_tone(lang)
    extra = ADVICE_EXTRA[lang]
    advice = list(advice_by_tone.get(tone, [extra["delay_decisions"], extra["choose_few"]]))

    signal_index = {signal["key"]: signal for signal in surfaced_signals}

    if signal_index.get("decision_timing", {}).get("status") == "caution":
        advice.insert(0, extra["delay_decisions"])
    if signal_index.get("politics", {}).get("level") == "high":
        advice.append(extra["tight_plans"])
    if signal_index.get("money", {}).get("level") == "high":
        advice.append(extra["money_write"])
    if signal_index.get("health", {}).get("level") == "high":
        advice.append(extra["protect_sleep"])
    if "relationships" in top_domains:
        advice.append(extra["say_awkward"])
    if "career_work" in top_domains:
        advice.append(extra["choose_few"])

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
        title = driver.get("_title", _driver_title_en(driver))
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


def _signal_payload(key: str, level: str, short_text: str, detail_text: str, lang: str) -> dict:
    signal_ui = get_signal_ui(lang)
    return {
        "key": key,
        "level": level,
        "emoji": signal_ui[key]["emoji"],
        "label": signal_ui[key]["label"],
        "short_text": short_text,
        "detail_text": detail_text,
    }


def _signal_strength(signal: dict) -> int:
    if signal["key"] == "decision_timing":
        return 2 if signal["status"] != "mixed" else 0
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


def _eclipse_name(planet: str, lang: str) -> str:
    names = ECLIPSE_NAMES[lang]
    return names["lunar"] if planet == "Moon" else names["solar"]


def _driver_title_en(driver: dict) -> str:
    """Fallback title using English labels (used when _title not set on driver)."""
    from app.core.config import HOUSE_MEANINGS
    event_label = {
        "eclipse": _eclipse_name(driver["planet"], "en"),
        "station": "station",
        "ingress": "sign change",
        "fallback": "background pattern",
    }[driver["event_type"]]

    if driver["event_type"] == "fallback":
        return f"{driver['planet']} background pattern"
    if driver["event_type"] == "eclipse":
        return f"{event_label} in {driver['sign']} / House {driver['house']}"
    return f"{driver['planet']} {event_label} in {driver['sign']} / House {driver['house']}"


def _driver_summary(planet: str, sign: str, house: int, event_type: str, motion: str | None, lang: str) -> str:
    templates = DRIVER_SUMMARY[lang]
    house_meanings = get_house_meanings(lang)

    if event_type == "eclipse":
        return templates["eclipse"].format(
            eclipse_name=_eclipse_name(planet, lang),
            house_meaning=house_meanings[house][0],
            sign=sign,
        )
    if event_type == "station" and motion == "retrograde":
        return templates["retrograde"].format(planet=planet, house=house)
    if event_type == "station":
        return templates["station"].format(planet=planet, house=house)
    if event_type == "ingress":
        return templates["ingress"].format(planet=planet, sign=sign, house=house)
    return templates["fallback"]


def _event_text(event_type: str, motion: str | None, lang: str) -> str:
    texts = EVENT_TEXT[lang]
    event_type_explanations = get_event_type_explanations(lang)

    if event_type == "station" and motion == "retrograde":
        return texts["retrograde"]
    if event_type == "station" and motion == "direct":
        return texts["direct"]
    return event_type_explanations[event_type]


def _combined_effect(planet: str, sign: str, house: int, event_type: str, motion: str | None, lang: str) -> str:
    templates = COMBINED_EFFECT[lang]
    sign_explanations = get_sign_explanations(lang)
    house_explanations = get_house_explanations(lang)
    sign_clause = sign_explanations.get(sign, FALLBACK_SIGN_TEXT[lang])
    house_clause = house_explanations[house]

    if event_type == "eclipse":
        return templates["eclipse"].format(planet=planet, sign_clause=sign_clause, house_clause=house_clause)
    if event_type == "station" and motion == "retrograde":
        return templates["retrograde"].format(planet=planet, sign_clause=sign_clause, house_clause=house_clause)
    if event_type == "station":
        return templates["station"].format(planet=planet, sign_clause=sign_clause, house_clause=house_clause)
    if event_type == "ingress":
        return templates["ingress"].format(planet=planet, sign_clause=sign_clause, house_clause=house_clause)
    return templates["fallback"].format(sign_clause=sign_clause, house_clause=house_clause)
