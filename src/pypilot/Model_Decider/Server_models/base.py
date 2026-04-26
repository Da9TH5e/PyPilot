# models/Local model/base.py
from pathlib import Path
import requests
from typing import Dict, Any, Optional
from pypilot.memory.chat_store import DataBaseStore


class BaseModel:
    def __init__(
        self,
        project_path: Optional[Path] = None,
        consent_given: Optional[bool] = None,
    ):
        self.project_id = None
        self.chat_store = None
        self.consent_given = consent_given

        if project_path:
            self.chat_store = DataBaseStore()
            self.chat_store.create_db()
            self.project_id = self.chat_store.get_or_create_project(
                str(project_path)
            )

    def answer(
        self,
    ) -> Optional[str]:
        raise NotImplementedError

class VPSModel(BaseModel):
    def __init__(
        self,
        project_path: Optional[Path] = None,
        consent_given: Optional[bool] = None,
    ):
        super().__init__(project_path, consent_given)


    def answer(
        self,
        question: str,
        *,
        provider: Optional[str] = None,
        context: Dict[str, Any],
        metadata: Optional[Dict[str, Any]],
    ) -> Optional[str]:

        memory_block = ""

        if self.chat_store and self.project_id:
            previous = self.chat_store.fetch_convo(self.project_id, limit=5)
            if previous:
                memory_block = "Previous conversation history:\n\n"
                for i, (q, a) in enumerate(previous, 1):
                    memory_block += f"Conversation {i}:\n"
                    memory_block += f"User: {q}\n"
                    memory_block += f"Assistant: {a}\n\n"

        prompt = ""

        if memory_block:
            prompt += (
                "PREVIOUS CONVERSATIONS:\n"
                "-----------------------\n"
                f"{memory_block}\n"
            )
        else:
            prompt += "There is no previous conversation.\n\n"

        prompt += (
            "CURRENT QUESTION:\n"
            "-----------------\n"
            f"{question}\n\n"
            "Answer the current question clearly. "
            "If it refers to previous conversation, use the information above."
        )

        try:
            res = requests.post("http://72.61.173.75:8002/api/ask", json={
                "context": context,
                "metadata": metadata,
                "prompt": prompt,
                "provider": provider
            })
            res.raise_for_status()
        except Exception as e:
            return f"[VPS ERROR] Failed to connect to the network service: {e}"

        raw_answer = res.json()
        answer = raw_answer["answer"]

        # ← Save to SQLite so next question has history
        if self.chat_store and self.project_id:
            self.chat_store.insert_convo(
                project_id=self.project_id,
                provider=provider or "unknown",
                question=question,
                answer=answer,
            )

        return answer