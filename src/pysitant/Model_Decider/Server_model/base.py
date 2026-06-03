# models/Local model/base.py
import os
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import urlparse, urlunparse

import requests
from dotenv import load_dotenv

from pysitant.memory.chat_store import DataBaseStore


load_dotenv()

VPS_API_URL_ENV = "PYSITANT_VPS_API_URL"
VPS_SESSION_URL_ENV = "PYSITANT_VPS_SESSION_URL"
VPS_API_KEY_ENV = "PYSITANT_API_KEY"
_session_token: Optional[str] = None


def get_vps_api_url() -> str:
    vps_api_url = os.getenv(VPS_API_URL_ENV)
    if not vps_api_url:
        raise RuntimeError(
            "VPS_API_URL is missing .Please reinstall this package."
        )
    return vps_api_url


def get_vps_session_url() -> str:
    session_url = os.getenv(VPS_SESSION_URL_ENV)
    if session_url:
        return session_url

    api_url = get_vps_api_url()
    parsed = urlparse(api_url)
    if parsed.path.endswith("/api/ask"):
        return urlunparse(parsed._replace(path=parsed.path[:-8] + "/session"))

    return api_url.rstrip("/") + "/session"


def get_vps_api_key() -> str:
    api_key = os.getenv(VPS_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            "Error Occurred from VPS side - API key is missing. Please reinstall the package and uninstall any previous versions."
        )
    return api_key


def get_session_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {get_vps_api_key()}",
        "Content-Type": "application/json",
    }


def reset_session_token() -> None:
    global _session_token
    _session_token = None


def get_session_token() -> Optional[str]:
    global _session_token
    if _session_token:
        return _session_token

    res = requests.post(
        get_vps_session_url(),
        headers=get_session_headers(),
        timeout=15,
    )
    res.raise_for_status()
    _session_token = res.json()["session_token"]
    
    if _session_token: return _session_token


def get_vps_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {get_session_token()}",
        "Content-Type": "application/json",
    }


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
    ) -> str:
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
    ) -> str:

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
            payload = {
                "context": context,
                "metadata": metadata,
                "prompt": prompt,
                "provider": provider,
            }
            res = requests.post(
                get_vps_api_url(),
                headers=get_vps_headers(),
                json=payload,
                timeout=60,
            )
            if res.status_code == 401:
                reset_session_token()
                res = requests.post(
                    get_vps_api_url(),
                    headers=get_vps_headers(),
                    json=payload,
                    timeout=60,
                )
            res.raise_for_status()
        except Exception as e:
            return f"Failed to connect to the network service"

        raw_answer = res.json()
        answer = raw_answer["answer"]

        if self.chat_store and self.project_id:
            self.chat_store.insert_convo(
                project_id=self.project_id,
                provider=provider or "unknown",
                question=question,
                answer=answer,
            )

        return answer
