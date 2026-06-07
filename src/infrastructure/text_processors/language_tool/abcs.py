from abc import ABC, abstractmethod


class ICustomDictionary(ABC):
    @abstractmethod
    def reload(self, words: set[str]) -> None:
        """Перезагружает слова в словарь исключений."""
        raise NotImplementedError

    @abstractmethod
    def contains(self, word: str) -> bool:
        raise NotImplementedError
