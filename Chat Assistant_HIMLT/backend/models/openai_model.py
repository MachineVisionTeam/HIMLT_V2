"""
OpenAI GPT-4o-mini model adapter (online).
"""

import os
from typing import List, Dict, Any

from .base import BaseModel


class OpenAIModel(BaseModel):
    """OpenAI GPT-4o-mini via API. Requires OPENAI_API_KEY and internet."""

    MODEL_ID = "gpt-4o-mini"

    @property
    def id(self) -> str:
        return "gpt-4o-mini"

    @property
    def name(self) -> str:
        return "gpt-4o-mini (online)"

    @property
    def is_online(self) -> bool:
        return True

    def is_available(self) -> bool:
        return bool(os.getenv("OPENAI_API_KEY", "").strip())

    def generate(self, messages: List[Dict[str, str]]) -> str:
        try:
            import openai
        except ImportError:
            raise ImportError("openai package required. Install: pip install openai")

        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not set. Add to .env or run: export OPENAI_API_KEY=sk-your-key"
            )

        # Support openai 1.x (OpenAI client) and 0.x (ChatCompletion.create)
        try:
            if hasattr(openai, "OpenAI"):
                client = openai.OpenAI(api_key=api_key, timeout=120.0)
                response = client.chat.completions.create(
                    model=self.MODEL_ID,
                    messages=messages,
                    temperature=0.3,
                    top_p=0.9,
                )
            else:
                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                    model=self.MODEL_ID,
                    messages=messages,
                    temperature=0.3,
                    top_p=0.9,
                )
            # Extract content (works for both 0.x and 1.x)
            choice = response.choices[0] if response.choices else None
            msg = getattr(choice, "message", choice) if choice else None
            content = getattr(msg, "content", None) if msg else None
            return (content or "").strip()
        except Exception as e:
            err = str(e)
            if "api_key" in err.lower() or "invalid" in err.lower() or "401" in err:
                raise ValueError("Invalid or missing OPENAI_API_KEY. Check your key at platform.openai.com")
            raise
