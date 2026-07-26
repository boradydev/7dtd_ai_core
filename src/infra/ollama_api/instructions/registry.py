from pathlib import Path

from src.app.common.ai.abcs import ISystemInstructions
from src.app.common.ai.behavior import AIBehavior
from src.app.common.utils.md_loader import MarkdownLoader


_md_louder = MarkdownLoader(Path(__file__).parent)


class SystemInstruction(ISystemInstructions[AIBehavior]):
    """Пресеты для системных промтов."""

    _PRESETS: dict[AIBehavior, str] = {
        AIBehavior.MODERATOR: _md_louder.load(file_path="prompts/moderator.md"),
        AIBehavior.ASSISTANT: _md_louder.load(file_path="prompts/assistant.md"),
        AIBehavior.STORYTELLER: _md_louder.load(file_path="prompts/storyteller.md"),
        AIBehavior.ENTERTAINER: _md_louder.load(file_path="prompts/entertainer.md"),
        AIBehavior.TOOL_ROUTER: _md_louder.load(file_path="prompts/tool_router.md"),
    }

    @classmethod
    def get(cls, behavior: AIBehavior) -> str:
        return cls._PRESETS[behavior]
