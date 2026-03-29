from statistics import mean
from typing import Protocol

from app.core.config import DOMAIN_LABELS, DOMAIN_EMOJIS, TONE_UI


class NarrativeProvider(Protocol):
    def generate_concise(self, period_data: dict) -> str:
        ...

    def generate_detailed(self, period_data: dict) -> str:
        ...


def attach_narratives(periods: list[dict], provider: NarrativeProvider) -> list[dict]:
    payload: list[dict] = []

    for period in periods:
        item = dict(period)
        item["concise_text"] = provider.generate_concise(item)
        item["detailed_text"] = provider.generate_detailed(item)
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
        summary = "A constructive year with more supportive windows than high-friction ones."
    elif stressful > supportive:
        summary = "A demanding year that rewards discipline, pacing, and selective commitments."
    else:
        summary = "A mixed year with alternating pressure and opportunity across the main life areas."

    top_themes = [f"{DOMAIN_EMOJIS[domain]} {DOMAIN_LABELS[domain]} stays prominent across multiple periods." for domain in top_domains]
    caution_periods = [
        f"{period['start_date']} to {period['end_date']}"
        for period in periods
        if period["tone"] in {"stressful", "volatile", "serious"}
    ][:3]
    opportunity_periods = [
        f"{period['start_date']} to {period['end_date']}"
        for period in periods
        if period["tone"] in {"supportive", "constructive", "expansive"}
    ][:3]

    tone_mix = {}
    for period in periods:
        tone_mix.setdefault(period["tone"], 0)
        tone_mix[period["tone"]] += 1
    top_tones = sorted(tone_mix, key=tone_mix.get, reverse=True)[:2]

    return {
        "summary": summary,
        "top_themes": top_themes,
        "tone_summary": [f"{TONE_UI[tone]['emoji']} {TONE_UI[tone]['label']}" for tone in top_tones],
        "confidence": round(mean(period["confidence"] for period in periods), 2),
        "top_caution_periods": caution_periods or ["No major caution periods flagged in the placeholder model."],
        "top_opportunity_periods": opportunity_periods or ["No major opportunity periods flagged in the placeholder model."],
    }
