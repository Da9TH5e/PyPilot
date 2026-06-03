# models/process.py
from pathlib import Path
from typing import Optional
from pysitant.Model_Decider.Server_model.base import VPSModel


class Checker:
    LIGHT_WORDS = {
        "explain", "what", "how", "tell", "find", "show",
        "list", "describe", "why", "who", "when", "where",
        "use of", "tell more"
    }

    def __init__(self, project_path: Optional[Path] = None):
        self.project_path = project_path

    def _contains_keywords(self, question: str, keywords: set) -> bool:
        q = question.lower()
        return any(word in q for word in keywords)

    def decide(self, question: str, context: dict | None = None) -> str:
        context = context or {}

        is_light = self._contains_keywords(question, self.LIGHT_WORDS)

        local_model = VPSModel(project_path=self.project_path)

        if is_light:
            return local_model.answer(
                question,
                provider="light",
                context=context,
                metadata={"reasoning": "light"},
            )

        return local_model.answer(
            question,
            provider="heavy",
            context=context,
            metadata={"reasoning": "heavy"},
        )