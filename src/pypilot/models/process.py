# models/process.py
from pathlib import Path
import socket
from typing import Optional
from pypilot.models.Local_model.base import LocalModel

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

	def decide(self, question: str, context: dict | None = None, heavy: bool = False) -> str:
		context = context or {}

		is_light = self._contains_keywords(question, self.LIGHT_WORDS)
		is_heavy = self._contains_keywords(question, self.HEAVY_WORDS)

		# if self._internet_available():
		# 	if is_heavy:
		# 		return "[VPS + Claude] -> Heavy task queued to claude"

		# 	if is_light:
		# 		return "[VPS + Groq] -> Light task queued to Groq"

		# 	return "[VPS] -> Default online handling....."


		# if is_heavy and not self._internet_available():
		# 	return (
		# 		"[OFFLINE MODE]\n"
		# 		"Heavy tasks are not recommended in offline mode."
		# 	)

		local_model = LocalModel(project_path=self.project_path)
		return local_model.answer(
			question,
			context = context,
			metadata = {"reason": "offline", "heavy": heavy},
		)
