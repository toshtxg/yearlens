from app.core.config import DOMAIN_LABELS, TONE_UI

_HEADLINE_VARIANTS = {
    "decision_timing": [
        "Use extra care before locking in major choices",
        "Pause before signing, committing, or promising",
        "Give big decisions more room to breathe",
        "Let important choices sit a little longer",
        "Timing is noisier here — avoid rushing anything permanent",
    ],
    "politics": [
        "Read people and politics more carefully",
        "Watch for mixed signals in group dynamics",
        "Navigate social currents with more caution",
    ],
    "relationships": [
        "Handle relationship dynamics more gently",
        "Be patient with emotional undercurrents",
        "Give close relationships a lighter touch",
    ],
    "money": [
        "Keep money decisions measured",
        "Take extra care around financial commitments",
        "Avoid impulsive spending or lending",
    ],
    "health": [
        "Slow down enough to protect energy and health",
        "Your body is asking for more margin here",
        "Watch for burnout — pace yourself deliberately",
    ],
    "travel": [
        "Movement and timing matter more here",
        "Travel or relocation plans need extra planning",
        "Give logistics and travel more buffer time",
    ],
    "work": [
        "Work pressure needs cleaner prioritization",
        "Focus on fewer things and do them well",
        "Career demands are louder — choose battles carefully",
    ],
}

_GOOD_TIMING_VARIANTS = [
    "A steadier window for clearer decisions",
    "Momentum is with you — act with intention",
    "This stretch favors forward movement",
]


def _pick_variant(variants: list[str], period_id: str, signal_key: str) -> str:
    index = hash((period_id, signal_key)) % len(variants)
    return variants[index]


class TemplateNarrativeProvider:
    def generate(self, period_data: dict) -> dict:
        primary_domain = DOMAIN_LABELS[period_data["top_domains"][0]].lower()
        tone_label = TONE_UI[period_data["tone"]]["label"].lower()
        primary_signal = period_data["surfaced_signals"][0] if period_data["surfaced_signals"] else None
        lead_driver = period_data["dominant_drivers"][0]
        period_id = period_data.get("id", "p0")

        return {
            "headline": _build_headline(primary_signal, primary_domain, tone_label, period_id),
            "concise_text": _build_concise_text(period_data, primary_domain, tone_label),
            "detailed_text": _build_detailed_text(period_data, lead_driver, primary_domain, tone_label),
        }


def _build_headline(primary_signal: dict | None, primary_domain: str, tone_label: str, period_id: str) -> str:
    if primary_signal is None:
        return f"{tone_label.capitalize()} focus on {primary_domain}"

    signal_key = primary_signal["key"]

    if signal_key == "decision_timing" and primary_signal["status"] == "good":
        return _pick_variant(_GOOD_TIMING_VARIANTS, period_id, "decision_timing_good")

    if signal_key in _HEADLINE_VARIANTS:
        return _pick_variant(_HEADLINE_VARIANTS[signal_key], period_id, signal_key)

    return f"{tone_label.capitalize()} focus on {primary_domain}"


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
