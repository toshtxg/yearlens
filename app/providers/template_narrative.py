from __future__ import annotations

import hashlib

from app.core.config import DOMAIN_LABELS, TONE_UI

_DOMAIN_FOCUS = {
    "career_work": "work priorities",
    "money_finance": "money decisions",
    "relationships": "close relationships",
    "health_emotional": "energy and emotional steadiness",
    "travel_overseas": "travel and timing",
    "study_growth": "learning and long-range plans",
}

_GOOD_TIMING_VARIANTS = {
    "default": [
        "This stretch is cleaner for forward moves",
        "Plans can move with less friction here",
        "The timing is steadier for important choices",
    ],
    "money_finance": [
        "Money choices can move more cleanly here",
        "This is a steadier stretch for practical financial decisions",
    ],
    "career_work": [
        "Work decisions can move more cleanly here",
        "This stretch gives career decisions a little more clarity",
    ],
    "relationships": [
        "Relationship decisions look a little clearer here",
        "This stretch is better for honest conversations and clearer choices",
    ],
}

_CAUTION_TIMING_VARIANTS = {
    "default": [
        "Give big decisions more breathing room",
        "Let important choices sit a little longer",
        "Avoid locking yourself in too quickly",
        "Go slower before making anything permanent",
    ],
    "money_finance": [
        "Let financial commitments breathe before you lock them in",
        "Go slower with money promises and practical commitments",
    ],
    "career_work": [
        "Delay major work commitments if they can wait",
        "Go slower before locking in career decisions",
    ],
    "relationships": [
        "Give relationship decisions more time before you commit",
        "Let emotional choices settle before you decide",
    ],
}

_SIGNAL_VARIANTS = {
    "politics": {
        "default": [
            "Read social dynamics more carefully",
            "Keep a closer eye on motives and alliances",
            "Go slower with politics and mixed agendas",
            "Be more selective about who gets access to your plans",
        ],
        "career_work": [
            "Navigate work politics with a steadier hand",
            "Keep office dynamics clearer and more deliberate",
        ],
    },
    "relationships": {
        "default": [
            "Give close ties a gentler pace",
            "Handle feelings and expectations more softly",
            "Let emotional reactions settle before responding",
            "Be patient with what is happening under the surface",
        ],
        "relationships": [
            "Go softer with relationship expectations",
            "Give close relationships a little more room to breathe",
        ],
        "health_emotional": [
            "Give feelings more room before reacting",
            "Let the emotional weather settle before you answer it",
        ],
    },
    "money": {
        "default": [
            "Take money choices one step at a time",
            "Keep financial commitments measured",
            "Slow down around spending, borrowing, or promises",
            "Treat practical decisions with a steadier hand",
        ],
        "money_finance": [
            "Be more deliberate with money and commitments",
            "Treat financial decisions with extra care",
        ],
    },
    "health": {
        "default": [
            "Give your energy more margin",
            "Protect rest before stress starts to spill over",
            "Go more gently with your body and nervous system",
            "Slow down enough to protect recovery",
        ],
        "health_emotional": [
            "Make more room for recovery and steadiness",
            "Protect your energy before it starts running thin",
        ],
    },
    "travel": {
        "default": [
            "Build more buffer into travel and timing",
            "Leave extra margin for movement and logistics",
            "Keep plans flexible when distance or timing matters",
            "Give travel, timing, and movement more breathing room",
        ]
    },
    "work": {
        "default": [
            "Narrow your workload to what matters most",
            "Choose priorities carefully and leave more margin",
            "Keep work demands tighter and more deliberate",
            "Do fewer things, but do the important ones well",
        ],
        "career_work": [
            "Trim the workload to what actually matters",
            "Give work pressure a cleaner set of priorities",
        ],
    },
}

_FALLBACK_VARIANTS = {
    "constructive": [
        "This stretch is easier to use well",
        "There is a little more forward movement here",
    ],
    "supportive": [
        "This stretch gives you more breathing room",
        "Support comes a little more easily here",
    ],
    "expansive": [
        "Growth is easier to lean into here",
        "This stretch opens the bigger picture a little wider",
    ],
    "stressful": [
        "Keep things simpler and more deliberate here",
        "This stretch rewards a slower hand",
    ],
    "serious": [
        "Treat this stretch with patience and structure",
        "This stretch asks for steadier pacing",
    ],
    "volatile": [
        "Stay flexible and do not overlock the plan",
        "Leave more room for shifts and changing conditions",
    ],
    "reflective": [
        "Give yourself more quiet margin here",
        "This stretch asks for more rest than force",
    ],
    "mixed": [
        "There is more nuance than urgency here",
        "Take this stretch one careful step at a time",
    ],
    "active": [
        "Move, but keep the details tidy",
        "This stretch works better with quick clarity than overthinking",
    ],
}


def _stable_index(seed: str, size: int) -> int:
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % size


def _pick_variant(variants: list[str], seed: str, recent_headlines: list[str]) -> str:
    if not variants:
        return ""

    start_index = _stable_index(seed, len(variants))
    ordered = [variants[(start_index + offset) % len(variants)] for offset in range(len(variants))]
    for candidate in ordered:
        if candidate not in recent_headlines:
            return candidate
    return ordered[0]


class TemplateNarrativeProvider:
    def __init__(self) -> None:
        self._recent_headlines: list[str] = []

    def generate(self, period_data: dict) -> dict:
        primary_domain_key = period_data["top_domains"][0]
        primary_domain = DOMAIN_LABELS[primary_domain_key].lower()
        tone_key = period_data["tone"]
        tone_label = TONE_UI[tone_key]["label"].lower()
        primary_signal = period_data["surfaced_signals"][0] if period_data["surfaced_signals"] else None
        lead_driver = period_data["dominant_drivers"][0]
        period_id = period_data.get("id", "p0")

        headline = _build_headline(
            primary_signal=primary_signal,
            primary_domain_key=primary_domain_key,
            tone_key=tone_key,
            lead_driver=lead_driver,
            period_id=period_id,
            recent_headlines=self._recent_headlines,
        )
        self._remember_headline(headline)

        return {
            "headline": headline,
            "concise_text": _build_concise_text(period_data, primary_domain, tone_label),
            "detailed_text": _build_detailed_text(period_data, lead_driver, primary_domain, tone_label),
        }

    def _remember_headline(self, headline: str) -> None:
        self._recent_headlines.append(headline)
        self._recent_headlines = self._recent_headlines[-3:]


def _build_headline(
    *,
    primary_signal: dict | None,
    primary_domain_key: str,
    tone_key: str,
    lead_driver: dict,
    period_id: str,
    recent_headlines: list[str],
) -> str:
    if primary_signal is None:
        fallback_variants = _fallback_variants_for_domain(tone_key, primary_domain_key)
        return _pick_variant(fallback_variants, f"{period_id}:{tone_key}:{primary_domain_key}", recent_headlines)

    signal_key = primary_signal["key"]
    seed = f"{period_id}:{signal_key}:{primary_domain_key}:{lead_driver.get('house')}:{lead_driver.get('event_type')}"

    if signal_key == "decision_timing":
        variants = _decision_timing_variants(primary_signal, primary_domain_key)
        return _pick_variant(variants, seed, recent_headlines)

    variants = _signal_variants(signal_key, primary_domain_key, lead_driver)
    if variants:
        return _pick_variant(variants, seed, recent_headlines)

    fallback_variants = _fallback_variants_for_domain(tone_key, primary_domain_key)
    return _pick_variant(fallback_variants, seed, recent_headlines)


def _decision_timing_variants(primary_signal: dict, primary_domain_key: str) -> list[str]:
    if primary_signal["status"] == "good":
        return _GOOD_TIMING_VARIANTS.get(primary_domain_key, []) + _GOOD_TIMING_VARIANTS["default"]
    return _CAUTION_TIMING_VARIANTS.get(primary_domain_key, []) + _CAUTION_TIMING_VARIANTS["default"]


def _signal_variants(signal_key: str, primary_domain_key: str, lead_driver: dict) -> list[str]:
    domain_variants = _SIGNAL_VARIANTS.get(signal_key, {})
    variants = list(domain_variants.get(primary_domain_key, []))
    variants.extend(domain_variants.get("default", []))

    house = lead_driver.get("house")
    if signal_key == "relationships" and house == 8:
        variants.insert(0, "Move more carefully with trust and emotional intensity")
    if signal_key == "relationships" and house == 7:
        variants.insert(0, "Go softer with relationship dynamics and expectations")
    if signal_key == "politics" and house in {11, 12}:
        variants.insert(0, "Keep your plans closer to the chest here")
    if signal_key == "money" and house == 8:
        variants.insert(0, "Be more deliberate with shared money and obligations")
    if signal_key == "health" and house in {6, 12}:
        variants.insert(0, "Protect your routine before stress starts to snowball")
    if signal_key == "travel" and house in {9, 12}:
        variants.insert(0, "Leave extra slack around distance, timing, and movement")
    if signal_key == "work" and house == 10:
        variants.insert(0, "Visible responsibilities need a steadier pace")

    return variants


def _fallback_variants_for_domain(tone_key: str, primary_domain_key: str) -> list[str]:
    focus = _DOMAIN_FOCUS.get(primary_domain_key, "the main priorities here")
    base = list(_FALLBACK_VARIANTS.get(tone_key, []))

    if tone_key in {"supportive", "constructive", "expansive"}:
        base.insert(0, f"There is more room to move with {focus} here")
    elif tone_key in {"stressful", "serious", "volatile", "reflective"}:
        base.insert(0, f"Go more deliberately with {focus} here")
    else:
        base.insert(0, f"This stretch puts more emphasis on {focus}")

    return base


def _build_concise_text(period_data: dict, primary_domain: str, tone_label: str) -> str:
    use_for = period_data["use_for"][0]
    careful_with = period_data["careful_with"][0] if period_data["careful_with"] else None

    summary = f"This {tone_label} window puts more emphasis on {primary_domain}. It is better used for {use_for}"
    if careful_with:
        summary += f", while using extra care around {careful_with}"
    return f"{summary}."


def _build_detailed_text(period_data: dict, lead_driver: dict, primary_domain: str, tone_label: str) -> str:
    use_for = "; ".join(period_data["use_for"][:2])
    careful_with = "; ".join(period_data["careful_with"][:2]) or "pushing too hard without enough margin"
    return (
        f"This {tone_label} stretch leans most strongly toward {primary_domain}. "
        f"The main driver is this: {lead_driver['summary']} "
        f"That makes this window better for {use_for}, while asking for more care around {careful_with}."
    )
