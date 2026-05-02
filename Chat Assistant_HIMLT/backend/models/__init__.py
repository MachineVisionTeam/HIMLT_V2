"""Model adapters for the Hybrid Multi-Model Chat Framework."""

from .base import BaseModel
from .openai_model import OpenAIModel
from .medllama_model import MedLLaMAModel
from .ollama_model import OllamaModel
from .registry import ModelRegistry, get_registry

__all__ = [
    "BaseModel",
    "OpenAIModel",
    "MedLLaMAModel",
    "OllamaModel",
    "ModelRegistry",
    "get_registry",
]
