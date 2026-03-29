from app.core.config import DOMAIN_LABELS, TONE_UI


class TemplateNarrativeProvider:
    def generate(self, period_data: dict) -> dict:
        primary_domain = DOMAIN_LABELS[period_data["top_domains"][0]].lower()
        tone_label = TONE_UI[period_data["tone"]]["label"].lower()
        primary_signal = period_data["surfaced_signals"][0] if period_data["surfaced_signals"] else None
        lead_driver = period_data["dominant_drivers"][0]

        return {
            "headline": _build_headline(primary_signal, primary_domain, tone_label),
            "concise_text": _build_concise_text(period_data, primary_domain, tone_label),
            "detailed_text": _build_detailed_text(period_data, lead_driver, primary_domain, tone_label),
        }


def _build_headline(primary_signal: dict | None, primary_domain: str, tone_label: str) -> str:
    if primary_signal is None:
        return f"{tone_label.capitalize()} focus on {primary_domain}"

    headline_by_signal = {
        "decision_timing": "Use extra care before locking in major choices",
        "politics": "Read people and politics more carefully",
        "relationships": "Handle relationship dynamics more gently",
        "money": "Keep money decisions measured",
        "health": "Slow down enough to protect energy and health",
        "travel": "Movement and timing matter more here",
        "work": "Work pressure needs cleaner prioritization",
    }

    if primary_signal["key"] == "decision_timing" and primary_signal["status"] == "good":
        return "A steadier window for clearer decisions"

    return headline_by_signal.get(primary_signal["key"], f"{tone_label.capitalize()} focus on {primary_domain}")


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
