from enum import Enum


class AIBehavior(str, Enum):
    """
    Режимы поведения ИИ-админа в глобальном чате.

    MODERATOR Строгий разбор команд, логов, токсичности (temp = 0.0)
    ASSISTANT Помощь игрокам по правилам, рецептам (temp = 0.3)
    STORYTELLER Генератор игровых ивентов, квестов, лора (temp = 0.7)
    ENTERTAINER Шутки, токсичные ответы зомби, флуд в чате (temp = 0.9).
    """

    MODERATOR = "moderator"
    ASSISTANT = "assistant"
    STORYTELLER = "storyteller"
    ENTERTAINER = "entertainer"
