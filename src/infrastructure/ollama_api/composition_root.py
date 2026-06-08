from src.application.common.ai.behavior import AIBehavior
from src.infrastructure.ollama_api.config import AIModelConfig
from src.infrastructure.ollama_api.instructions import SystemInstruction
from src.infrastructure.ollama_api.sdk_tools import AIService
from src.infrastructure.ollama_api.tools import AITools
from src.settings import AppSettings


def provide_ai_service(settings: AppSettings) -> AIService[AIBehavior]:
    return AIService[AIBehavior](
        host=settings.AI_API_URL,
        instructions=SystemInstruction,
        options=AIModelConfig,
        tools_provider=AITools,
        model_name="llama3.1",
    )
