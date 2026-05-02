"""
Generic Ollama model adapter. Supports any model pulled in Ollama.
"""

import json
import os
from typing import List, Dict, Any

from .base import BaseModel


class OllamaModel(BaseModel):
    """Any Ollama model. Requires: ollama serve, and model pulled."""

    def __init__(self, model_id: str, display_name: str = None):
        self._model_id = model_id
        self._display_name = display_name or model_id

    @property
    def id(self) -> str:
        return self._model_id.replace("/", "-").replace(":", "-")

    @property
    def name(self) -> str:
        return f"{self._display_name} (offline)"

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
                f"Cannot reach Ollama. Start: ollama serve. Pull model: ollama pull {self._model_id}"
            ) from e
        except HTTPError as e:
            raise RuntimeError(f"Ollama request failed: {e}") from e

        msg = data.get("message") or {}
        return (msg.get("content") or "").strip()
