#context_store.py
import json
from pathlib import Path

class ContextStore:
	def __init__(self, project_path: Path):
		self.project_path = project_path
		self.context_dir = project_path / ".pypilot"
		self.filename = self.context_dir / "context.json"
	
	def exists(self) -> bool:
		return self.filename.exists()

	def save(self, data: dict):
		self.context_dir.mkdir(parents=True, exist_ok=True)
		with self.filename.open("w", encoding="utf-8") as file:
			json.dump(data, file, indent=2)

	def load(self) -> dict:
		if not self.exists():
			raise FileNotFoundError(
				"No context for the project is found. Run the pypilot to build a context first."
				)

		with self.filename.open("r", encoding="utf-8") as file:
			return json.load(file)