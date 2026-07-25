from abc import ABC, abstractmethod

from src.app.game_data.common.localization.languages import LocalizationLanguage
from src.app.game_data.dtos import MatchedItemDTO, RecipeDTO
from src.app.game_data.schemas.localization import LocalizationGameData
from src.app.game_data.schemas.recipes import RecipeGameData
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
    async def clear(self) -> None:
        """Отчищает таблицу."""
        raise NotImplementedError

    @abstractmethod
    async def list_by_key(self, key: str) -> list[RecipeDTO]:
        """
        Retrieve all available crafting recipes and ingredient requirements
        for a specific item by its unique internal key.

        Use this tool as the SECOND STEP only after you have obtained a valid,
        single item key from the 'search_by_fuzzy' tool.
        Do NOT guess or hallucinate the key.
        This tool returns the exact ingredients, required quantities, crafting stations,
        and player skills needed to create the item in 7 Days to Die.

        Args:
            key: The exact internal unique identifier of the item obtained from
            'search_by_fuzzy' (e.g., "meleeWeaponIronAxe", "medicalFirstAidBandage").
        """
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


class IItemsRepository(ABC):
    @abstractmethod
    async def search_by_fuzzy(
        self,
        text: str,
        lang: LocalizationLanguage,
    ) -> list[MatchedItemDTO]:
        """
        Fuzzy search for in-game item keys and titles in 7 Days to Die.

        Use this tool ALWAYS as the FIRST STEP when a player asks about crafting recipes,
        required ingredients, blueprints, or creation requirements for any item.
        This tool does NOT return the recipe itself; it returns a list of matching items
        and their internal keys. Use these keys later to fetch the exact recipe.

        Args:
            text: The full or partial name of the item to search for
                (e.g., "iron axe", "first aid bandage", "frame").
            lang: The language to search in. Must be either "russian" or "english"
                depending on the language used by the player.
        """
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

    @property
    @abstractmethod
    def items(self) -> IItemsRepository:
        """Требует репозиторий для предметов."""
        raise NotImplementedError


class IGameDataExtractor(ABC):
    @abstractmethod
    def recipes(self) -> list[RecipeGameData]:
        """Данные рецептов."""
        raise NotImplementedError

    @abstractmethod
    def localization(self) -> list[LocalizationGameData]:
        """Данные локализаций."""
        raise NotImplementedError
