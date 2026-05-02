"""
Model registry: collects model classes and exposes list_models(), get_model_by_id().
Plug-and-play: add new model classes to extend the framework.
Presets: gpt-4o-mini, medllama2, medichat-llama3, medexpert, etc.
"""

from typing import List, Optional, Type, Tuple

from .base import BaseModel
from .openai_model import OpenAIModel
from .medllama_model import MedLLaMAModel
from .ollama_model import OllamaModel

# (model_class, init_args) for models that need constructor args
# id is derived from the model
# (ollama_model_id, display_name) - medllama3 handled by MedLLaMAModel
OLLAMA_PRESETS: List[Tuple[str, str]] = [
    ("medllama2", "medllama2"),
    ("meditron", "meditron"),
    ("OussamaELALLAM/MedExpert", "medexpert"),
]


def _make_ollama_models():
    """Create Ollama model instances from presets."""
    return [OllamaModel(mid, name) for mid, name in OLLAMA_PRESETS]


class ModelRegistry:
    """Registry of available models. Use list_models() and get_model_by_id()."""

    def __init__(self):
        self._instances: dict[str, BaseModel] = {}
        for cls in [OpenAIModel, MedLLaMAModel]:
            try:
                inst = cls()
                self._instances[inst.id] = inst
            except Exception:
                pass
        for inst in _make_ollama_models():
            try:
                self._instances[inst.id] = inst
            except Exception:
                pass

    def list_models(self) -> List[BaseModel]:
        """Return all registered model instances."""
        return list(self._instances.values())

    def get_model_by_id(self, model_id: str) -> Optional[BaseModel]:
        """Get model by id (e.g. 'gpt-4o-mini', 'medllama3')."""
        return self._instances.get(model_id)

    def list_available_ids(self) -> List[str]:
        """Return ids of models that are currently available."""
        return [m.id for m in self._instances.values() if m.is_available()]


# Singleton registry
_registry: Optional[ModelRegistry] = None


def get_registry() -> ModelRegistry:
    """Return the global model registry."""
    global _registry
    if _registry is None:
        _registry = ModelRegistry()
    return _registry
