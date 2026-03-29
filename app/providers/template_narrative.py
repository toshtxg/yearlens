from app.core.config import DOMAIN_LABELS, TONE_UI


class TemplateNarrativeProvider:
    def generate_concise(self, period_data: dict) -> str:
        primary = DOMAIN_LABELS[period_data["top_domains"][0]].lower()
        advice = period_data["advice"][0]
        tone_label = TONE_UI[period_data["tone"]]["label"].lower()
        article = "an" if tone_label[:1] in {"a", "e", "i", "o", "u"} else "a"
        return f"{article.capitalize()} {tone_label} period with emphasis on {primary}. {advice}"

    def generate_detailed(self, period_data: dict) -> str:
        driver = period_data["drivers"][0]
        primary = ", ".join(DOMAIN_LABELS[domain] for domain in period_data["top_domains"][:2]).lower()
        tone_label = TONE_UI[period_data["tone"]]["label"].lower()
        return (
            f"{driver['planet']} is emphasized through house {driver['house']}, bringing forward "
            f"{driver['planet_meaning']} themes around {driver['house_meaning']}. "
            f"This points to a {tone_label} stretch focused on {primary}. "
            f"{driver['combined_effect']}"
        )
