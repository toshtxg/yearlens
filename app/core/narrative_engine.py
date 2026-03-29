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
    for period in periods:
        for key, value in period["domains"].items():
            aggregate[key] += value

    top_domains = sorted(aggregate, key=aggregate.get, reverse=True)[:3]
    stressful = sum(1 for period in periods if period["tone"] in {"stressful", "volatile", "serious"})
    supportive = sum(1 for period in periods if period["tone"] in {"supportive", "constructive", "expansive"})

    if supportive > stressful:
        summary = "A year with some steadier windows for progress, as long as you use the sharper periods more carefully."
    elif stressful > supportive:
        summary = "A more demanding year that rewards pacing, clearer boundaries, and better timing."
    else:
        summary = "A mixed year with alternating stretches of pressure, reset, and usable momentum."

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
