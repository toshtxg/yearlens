from collections import Counter
from statistics import mean
from typing import Protocol

from app.core.config import DOMAINS, DOMAIN_EMOJIS, DOMAIN_LABELS, TONE_UI


class NarrativeProvider(Protocol):
    def generate(self, period_data: dict) -> dict:
        ...


def attach_narratives(periods: list[dict], provider: NarrativeProvider) -> list[dict]:
    payload: list[dict] = []

    for period in periods:
        item = dict(period)
        item.update(provider.generate(item))
        payload.append(item)

    return payload


def build_year_overview(periods: list[dict]) -> dict:
    aggregate = {key: 0 for key in DOMAIN_LABELS}
    signal_counts: Counter[str] = Counter()
    for period in periods:
        for key, value in period["domains"].items():
            aggregate[key] += value
        for signal in period.get("surfaced_signals", []):
            if signal["key"] != "decision_timing":
                signal_counts[signal["key"]] += 1

    top_domains = sorted(aggregate, key=aggregate.get, reverse=True)[:3]
    stressful = sum(1 for period in periods if period["tone"] in {"stressful", "volatile", "serious"})
    supportive = sum(1 for period in periods if period["tone"] in {"supportive", "constructive", "expansive"})

    top_themes = [f"{DOMAIN_EMOJIS[domain]} {DOMAIN_LABELS[domain]} comes up repeatedly across the year." for domain in top_domains]
    caution_periods = [
        f"{period['start_date']} to {period['end_date']} · {period['headline']}"
        for period in periods
        if period["tone"] in {"stressful", "volatile", "serious"}
    ][:3]
    opportunity_periods = [
        f"{period['start_date']} to {period['end_date']} · {period['headline']}"
        for period in periods
        if period["tone"] in {"supportive", "constructive", "expansive"}
    ][:3]

    tone_mix = {}
    for period in periods:
        tone_mix.setdefault(period["tone"], 0)
        tone_mix[period["tone"]] += 1
    ordered_tones = sorted(tone_mix.items(), key=lambda item: item[1], reverse=True)
    leading_signal = signal_counts.most_common(1)[0][0] if signal_counts else None
    summary = _build_year_summary(top_domains, supportive, stressful, ordered_tones, leading_signal)

    return {
        "summary": summary,
        "top_themes": top_themes,
        "tone_summary": [
            {
                "tone": tone,
                "label": TONE_UI[tone]["label"],
                "emoji": TONE_UI[tone]["emoji"],
                "count": count,
            }
            for tone, count in ordered_tones
        ],
        "confidence": round(mean(period["confidence"] for period in periods), 2),
        "domain_totals": {
            domain: round(sum(period["domains"][domain] for period in periods) / len(periods), 1)
            for domain in DOMAINS
        },
        "top_caution_periods": caution_periods or ["No strong caution windows were surfaced from the current ruleset."],
        "top_opportunity_periods": opportunity_periods or ["No unusually supportive windows were surfaced from the current ruleset."],
    }


def _build_year_summary(
    top_domains: list[str],
    supportive: int,
    stressful: int,
    ordered_tones: list[tuple[str, int]],
    leading_signal: str | None,
) -> str:
    domain_phrase = _domain_focus_phrase(top_domains[:2])
    lead_tone = ordered_tones[0][0] if ordered_tones else None

    intro = f"This year brings more focus to {domain_phrase}."
    middle = _year_middle_sentence(supportive, stressful, lead_tone)

    signal_sentence = _signal_sentence(leading_signal)
    return f"{intro} {middle}{signal_sentence}"


def _year_middle_sentence(supportive: int, stressful: int, lead_tone: str | None) -> str:
    if supportive >= stressful + 2:
        if lead_tone == "volatile":
            return "Overall, there is room for progress, but plans may change faster than expected, so flexibility will help."
        if lead_tone == "supportive":
            return "Overall, there is usable momentum here, especially when you build on what is already working."
        return "Overall, the year looks more open than blocked, and the steadier stretches are worth using well."

    if stressful >= supportive + 2:
        if lead_tone == "volatile":
            return "Overall, it may feel more demanding and less predictable than easy, so staying flexible will help more than forcing things."
        if lead_tone == "reflective":
            return "Overall, it may feel slower and heavier than easy, so patience and self-awareness will help more than pushing."
        return "Overall, it may feel a little heavier than easy, so pacing yourself and choosing your timing well will help."

    if lead_tone == "volatile":
        return "Overall, the year looks mixed and somewhat changeable, so staying flexible will help more than locking in too quickly."
    if lead_tone == "supportive":
        return "Overall, the year looks mixed, but there are still some supportive stretches you can build on."
    if lead_tone == "reflective":
        return "Overall, the year looks mixed, with some slower stretches that may ask for patience and more inner space."
    return "Overall, the year looks mixed, with some stretches that flow and others that need more care."


def _domain_focus_phrase(domains: list[str]) -> str:
    phrases = {
        "career_work": "work, direction, and responsibility",
        "money_finance": "money, security, and practical decisions",
        "relationships": "relationships, closeness, and expectations",
        "health_emotional": "health, emotional balance, and recovery",
        "travel_overseas": "travel, movement, and wider horizons",
        "study_growth": "learning, perspective, and personal growth",
    }

    selected = [phrases[domain] for domain in domains if domain in phrases]
    if not selected:
        return "a few different parts of life"
    if len(selected) == 1:
        return selected[0]
    return f"{selected[0]}, along with {selected[1]}"


def _signal_sentence(signal_key: str | None) -> str:
    if signal_key is None:
        return ""

    phrases = {
        "politics": " People dynamics may need a little more discernment than usual.",
        "relationships": " Relationships may need more gentleness and clearer expectations.",
        "money": " Money decisions are worth handling a little more deliberately.",
        "health": " Energy and stress are worth paying closer attention to.",
        "travel": " Travel, movement, or timing may come up more than usual.",
        "work": " Workload and responsibility may take up more space than usual.",
    }
    return phrases.get(signal_key, "")
