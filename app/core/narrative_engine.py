from statistics import mean
from typing import Protocol

from app.core.config import DOMAINS, DOMAIN_EMOJIS, get_domain_labels, get_tone_ui
from app.core.meaning_strings import YEAR_OVERVIEW


class NarrativeProvider(Protocol):
    def generate(self, period_data: dict, lang: str = "en") -> dict:
        ...


def attach_narratives(periods: list[dict], provider: NarrativeProvider, lang: str = "en") -> list[dict]:
    payload: list[dict] = []

    for period in periods:
        item = dict(period)
        item.update(provider.generate(item, lang))
        payload.append(item)

    return payload


def build_year_overview(periods: list[dict], lang: str = "en") -> dict:
    domain_labels = get_domain_labels(lang)
    tone_ui = get_tone_ui(lang)
    overview_text = YEAR_OVERVIEW[lang]

    aggregate = {key: 0 for key in domain_labels}
    for period in periods:
        for key, value in period["domains"].items():
            aggregate[key] += value

    top_domains = sorted(aggregate, key=aggregate.get, reverse=True)[:3]
    stressful = sum(1 for period in periods if period["tone"] in {"stressful", "volatile", "serious"})
    supportive = sum(1 for period in periods if period["tone"] in {"supportive", "constructive", "expansive"})

    if supportive > stressful:
        summary = overview_text["steady"]
    elif stressful > supportive:
        summary = overview_text["demanding"]
    else:
        summary = overview_text["mixed"]

    top_themes = [
        overview_text["theme_template"].format(emoji=DOMAIN_EMOJIS[domain], domain=domain_labels[domain])
        for domain in top_domains
    ]
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
                "label": tone_ui[tone]["label"],
                "emoji": tone_ui[tone]["emoji"],
                "count": count,
            }
            for tone, count in ordered_tones
        ],
        "confidence": round(mean(period["confidence"] for period in periods), 2),
        "domain_totals": {
            domain: round(sum(period["domains"][domain] for period in periods) / len(periods), 1)
            for domain in DOMAINS
        },
        "top_caution_periods": caution_periods or [overview_text["no_caution"]],
        "top_opportunity_periods": opportunity_periods or [overview_text["no_opportunity"]],
    }
