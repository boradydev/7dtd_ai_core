import pytest

from src.infra.ollama_api.config import AIModelConfig
from src.infra.ollama_api.instructions import SystemInstruction
from src.infra.ollama_api.api import OllamaApi


@pytest.fixture
def ai_service():
    return OllamaApi(
        host="http://192.168.1.108:11434",
        instructions=SystemInstruction,
        options=AIModelConfig,
        model_name="llama3.1",
    )
