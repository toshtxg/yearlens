class LLMNarrativeProvider:
    def generate(self, period_data: dict) -> dict:
        del period_data
        raise NotImplementedError("LLM narrative provider is not wired yet.")
