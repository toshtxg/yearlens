from app.core.config import DOMAIN_LABELS


class TemplateNarrativeProvider:
    def generate_concise(self, period_data: dict) -> str:
        primary = DOMAIN_LABELS[period_data["top_domains"][0]].lower()
        advice = period_data["advice"][0]
        return f"A {period_data['tone']} period with emphasis on {primary}. {advice}"

    def generate_detailed(self, period_data: dict) -> str:
        driver = period_data["drivers"][0]
        primary = ", ".join(DOMAIN_LABELS[domain] for domain in period_data["top_domains"][:2]).lower()
        return (
            f"{driver['planet']} is emphasized through house {driver['house']}, bringing forward "
            f"{driver['planet_meaning']} themes around {driver['house_meaning']}. "
            f"This points to a {period_data['tone']} stretch focused on {primary}. "
            f"{driver['combined_effect']}"
        )

