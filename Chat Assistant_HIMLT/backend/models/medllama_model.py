"""
MedLLaMA 3 offline model adapter via Ollama.
Uses medichat-llama3 (medical Llama 3) when run through Ollama.
"""

import json
import os
from typing import List, Dict, Any

from .base import BaseModel


# Default Ollama model for medical use. Override with LLM_OFFLINE_AUTO_MODEL.
# Use full name for Ollama: monotykamary/medichat-llama3 (or shorter if pulled locally)
DEFAULT_OLLAMA_MODEL = "monotykamary/medichat-llama3"


class MedLLaMAModel(BaseModel):
    """
    MedLLaMA 3 via Ollama. Requires: ollama serve, and model pulled (e.g. ollama pull medichat-llama3).
    """

    def __init__(self, model_id: str = None):
        self._model_id = (
            (os.getenv("LLM_OFFLINE_AUTO_MODEL") or "").strip()
            or model_id
            or DEFAULT_OLLAMA_MODEL
        )

    @property
    def id(self) -> str:
        return "medllama3"

    @property
    def name(self) -> str:
        return "medllama3 (offline)"

    @property
    def is_online(self) -> bool:
        return False

    def is_available(self) -> bool:
        try:
            from urllib.request import urlopen
            url = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/") + "/api/tags"
            with urlopen(url, timeout=5) as _:
                return True
        except Exception:
            return False

    def generate(self, messages: List[Dict[str, str]]) -> str:
        from urllib.request import Request, urlopen
        from urllib.error import URLError, HTTPError

        url = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/") + "/api/chat"
        body = json.dumps({
            "model": self._model_id,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.3, "top_p": 0.9},
        }).encode("utf-8")
        req = Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})
        try:
            with urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except URLError as e:
            reason = getattr(e, "reason", str(e))
            raise ConnectionError(
                f"Cannot reach Ollama at {url}. ({reason}) Start: ollama serve. Pull model: ollama pull {self._model_id}"
            ) from e
        except HTTPError as e:
            raise RuntimeError(f"Ollama request failed: {e}") from e

        msg = data.get("message") or {}
        return (msg.get("content") or "").strip()
