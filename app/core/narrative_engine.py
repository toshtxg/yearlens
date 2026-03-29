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
    domain_phrase, verb = _domain_phrase(top_domains[:2])
    lead_tone = ordered_tones[0][0] if ordered_tones else None

    if supportive >= stressful + 2:
        rhythm = "The rhythm is more open than blocked overall"
        guidance = "use the steadier stretches to move things forward without overextending."
    elif stressful >= supportive + 2:
        rhythm = "The rhythm runs more demanding than light"
        guidance = "pacing, clearer boundaries, and better timing matter more than forcing results."
    else:
        rhythm = "The rhythm shifts between supportive and sharper stretches"
        guidance = "you will get better results by adjusting pace instead of treating the whole year the same."

    if lead_tone == "reflective":
        guidance = "slowing down, listening to what is changing internally, and choosing timing carefully will help more than pushing."
    elif lead_tone == "supportive":
        guidance = "there is usable momentum here, especially when you build on what is already working."
    elif lead_tone == "volatile":
        guidance = "staying flexible and resisting rushed reactions will matter more than trying to control every turn."

    signal_sentence = _signal_sentence(leading_signal)
    return f"{domain_phrase} {verb} more of the story this year. {rhythm}, so {guidance}{signal_sentence}"


def _domain_phrase(domains: list[str]) -> tuple[str, str]:
    labels = [DOMAIN_LABELS[domain] for domain in domains if domain in DOMAIN_LABELS]
    if not labels:
        return "A few different areas", "carry"
    if len(labels) == 1:
        return labels[0], "carries"
    return f"{labels[0]} and {labels[1]}", "carry"


def _signal_sentence(signal_key: str | None) -> str:
    if signal_key is None:
        return ""

    phrases = {
        "politics": " Repeated pressure also shows up around people dynamics, mixed motives, or social friction.",
        "relationships": " Close relationships and expectations may need a lighter touch than usual.",
        "money": " Money choices and practical commitments look worth handling more deliberately.",
        "health": " Energy, stress, and emotional load are worth paying closer attention to.",
        "travel": " Movement, timing, or distance-related plans look more prominent than usual.",
        "work": " Workload, responsibility, and prioritization carry extra weight in the year.",
    }
    return phrases.get(signal_key, "")
