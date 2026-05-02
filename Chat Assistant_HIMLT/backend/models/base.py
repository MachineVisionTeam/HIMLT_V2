"""
Base model interface for the Hybrid Multi-Model Chat Framework.
All model adapters must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseModel(ABC):
    """Abstract base class for LLM model adapters."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the model (e.g. 'gpt-4o-mini', 'medllama3')."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable display name (e.g. 'gpt-4o-mini (online)')."""
        pass

    @property
    def is_online(self) -> bool:
        """True if this model requires internet/API; False for local models."""
        return True

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the model can be used right now.
        For online: API key set + (optionally) internet reachable.
        For offline: local server/process reachable.
        """
        pass

    @abstractmethod
    def generate(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response given a list of messages.
        messages: [{"role": "user"|"assistant"|"system", "content": "..."}, ...]
        Returns: response text string.
        """
        pass
