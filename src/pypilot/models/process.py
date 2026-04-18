# models/process.py
from pathlib import Path
import socket
from typing import Optional
from pypilot.models.Local_model.base import VPSModel

class Checker:
	HEAVY_WORDS = {"create", "detailed", "details", "detail", "structured", "generate"}
	LIGHT_WORDS = {"explain", "use of", "tell more", "find"}

	def __init__(self, consent_given: bool, project_path: Optional[Path] = None):
		self.project_path = project_path
		self.consent_given = consent_given

	def _internet_available(self, timeout: float = 2.0) -> bool:
		try:
			socket.create_connection(("8.8.8.8", 53), timeout=timeout)
			return True
		except OSError:
			return False

	def _contains_keywords(self, question: str, keywords: set[str]) -> bool :
		q = question.lower()
		return any(word in q for word in keywords)

	def decide(self, question: str, context: dict | None = None) -> str:
		context = context or {}

		is_light = self._contains_keywords(question, self.LIGHT_WORDS)

		local_model = VPSModel(project_path=self.project_path)

		if is_light:
			return local_model.answer(
				question,
				provider = "groq",
				context = context,
				metadata = {"reasoning": "light"},
			)
   
		return local_model.answer(
			question,
			provider = "claude",
			context = context,
			metadata = {"reasoning": "heavy"},
		)