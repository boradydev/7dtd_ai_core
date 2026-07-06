from abc import ABC, abstractmethod

from src.application.game_data.dtos import RecipeDTO
from src.application.game_data.schemas.localization import LocalizationGameData
from src.application.game_data.schemas.recipes import RecipeGameData
from src.domain.common.abcs import InterfaceUOW


class IRecipesRepository(ABC):
    @abstractmethod
    async def add_many(
        self,
        dtos: list[RecipeGameData],
    ) -> None:
        """Добавляет список рецептов."""
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, recipe_name: str) -> list[RecipeDTO]:
        """Ищет все рецепты предмета."""
        raise NotImplementedError

    @abstractmethod
    async def clear(self) -> None:
        """Отчищает таблицу."""
        raise NotImplementedError


class ILocalizationRepository(ABC):
    @abstractmethod
    async def add_many(
        self,
        dtos: list[LocalizationGameData],
    ) -> None:
        """Добавляет список локализаций."""
        raise NotImplementedError

    @abstractmethod
    async def clear(self) -> None:
        """Отчищает таблицу."""
        raise NotImplementedError


class IGameDataUOW(InterfaceUOW, ABC):
    @property
    @abstractmethod
    def recipes(self) -> IRecipesRepository:
        """Требует репозиторий для рецептов крафта."""
        raise NotImplementedError

    @property
    @abstractmethod
    def localization(self) -> ILocalizationRepository:
        """Требует репозиторий для локализаций."""
        raise NotImplementedError


class IGameDataExtractor(ABC):
    @abstractmethod
    def recipes(self) -> list[RecipeGameData]:
        """Данные рецептов."""
        raise NotImplementedError

    @abstractmethod
    def localization(self) -> LocalizationGameData:
        """Данные рецептов."""
        raise NotImplementedError
