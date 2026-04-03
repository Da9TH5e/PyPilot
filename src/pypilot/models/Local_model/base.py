# models/Local model/base.py
<<<<<<< HEAD
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
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
            self.chat_store = DataBaseStore(project_path)
            self.chat_store.create_db()
            self.project_id = self.chat_store.get_or_create_project(
                str(project_path)
            )

=======
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Dict, Any, Optional


class BaseModel:
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4
    def answer(
        self,
        question: str,
        *,
        context: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        raise NotImplementedError

<<<<<<< HEAD
class LocalModel(BaseModel):
    MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"

    def __init__(
        self,
        project_path: Optional[Path] = None,
        consent_given: Optional[bool] = None,
    ):
        super().__init__(project_path, consent_given)
=======

class LocalModel(BaseModel):
    MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"

    def __init__(self):
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4
        self._tokenizer: Optional[Any] = None
        self._model: Optional[Any] = None
        self._loaded = False

    def _load_model(self) -> None:
        if self._loaded:
            return

        try:
            self._tokenizer = AutoTokenizer.from_pretrained(self.MODEL_ID)
            self._model = AutoModelForCausalLM.from_pretrained(self.MODEL_ID)
            self._loaded = True
        except Exception as e:
            raise RuntimeError(
                f"Failed to load model {self.MODEL_ID}\n\n{e}"
            )

    def answer(
        self,
        question: str,
        *,
        context: Dict[str, Any],
        metadata: Optional[Dict[str, Any]],
    ) -> str:
        try:
            self._load_model()
        except RuntimeError as e:
            return (
                "[LOCAL MODEL ERROR]\n"
                "The local language model could not be loaded.\n\n"
                f"{e}"
            )

<<<<<<< HEAD
        memory_block = ""

        if self.chat_store and self.project_id:
            previous = self.chat_store.fetch_convo(self.project_id, limit=5)

            if previous:
                memory_block = "Previous conversation history:\n\n"
                for i, (q, a) in enumerate(previous, 1):
                    memory_block += f"Conversation {i}:\n"
                    memory_block += f"User: {q}\n"
                    memory_block += f"Assistant: {a}\n\n"

        prompt = "You are an ssistant helping with a project.\n\n"

        if memory_block:
            prompt += (
                "PREVIOUS CONVERSATIONS: \n"
                "-------------------------\n"
                f"{memory_block}\n"
            )
        else:
            prompt += "There is no previous converstion. \n\n"

        prompt += (
            "CURRENT QUESTION: \n"
            "------------------\n"
            f"{question}\n\n"

            "Answer the current question clearly. "
            "If it refers to previous conversation, use the information above."
        )

        messages = [
            {
                "role": "user", "content": prompt
            }
=======
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a small local language model running offline. "
                    "Your answers must be short, cautious, and honest. "
                    "If unsure, say you are unsure."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4
        ]

        try:
            if self._tokenizer is None or self._model is None:
                raise RuntimeError("Model not loaded properly")
            
            inputs = self._tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_tensors="pt",
                return_dict=True,
            )

            inputs = {k: v.to(self._model.device) for k, v in inputs.items()}

            outputs = self._model.generate(
                **inputs,
                max_new_tokens=128,
                do_sample=True,
                temperature=0.7,
            )

            generated = self._tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[-1]:],
                skip_special_tokens=True,
            )

<<<<<<< HEAD
            raw_answer = generated.strip()
            
=======
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4
        except Exception as e:
            return (
                "[LOCAL MODEL ERROR]\n"
                "The local model failed during inference.\n\n"
                f"{e}"
            )

<<<<<<< HEAD
        disply_answer = (
                "[LOCAL MODEL — LIMITED]\n"
                "This answer was generated by a small offline model "
                "and may be incomplete or inaccurate.\n\n"
                f"{raw_answer}"
            )

        if self.chat_store and self.project_id:
            self.chat_store.insert_convo(
                project_id=self.project_id,
                provider="local",
                question=question,
                answer=raw_answer,
            )

        return disply_answer
=======
        return (
            "[LOCAL MODEL — LIMITED]\n"
            "This answer was generated by a small offline model "
            "and may be incomplete or inaccurate.\n\n"
            f"{generated.strip()}"
        )
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4
