class LLMNarrativeProvider:
    def generate_concise(self, period_data: dict) -> str:
        del period_data
        raise NotImplementedError("LLM narrative provider is not wired yet.")

    def generate_detailed(self, period_data: dict) -> str:
        del period_data
        raise NotImplementedError("LLM narrative provider is not wired yet.")

