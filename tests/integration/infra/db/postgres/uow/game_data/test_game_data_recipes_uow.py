import pytest

from src.app.game_data.common.localization.languages import LocalizationLanguage
from src.app.game_data.schemas.recipes import RecipesGameData
from src.infra.xml_parser.common.parser import UniversalXmlParser
from src.infra.xml_parser.patterns.recipes import PATTERN


@pytest.fixture
async def loaded_recipes(game_data_uow, config_dir) -> None:
    file_path = config_dir / "recipes.xml"

    parser = UniversalXmlParser(
        file_path=file_path,
        pattern=PATTERN,
    )

    game_data = RecipesGameData.model_validate(parser.run())

    async with game_data_uow as uow:
        await uow.recipes.clear()

        recipes = [recipe for recipe in game_data.recipes if recipe.is_craftable]

        await uow.recipes.add_many(recipes)
        await uow.commit()


@pytest.mark.timeout(1)
async def test_game_data_recipes_search_by_fuzzy_returns_results(
    loaded_recipes,
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.recipes.search_by_fuzzy(
            text="pistol",
            lang=LocalizationLanguage.ENGLISH,
        )

    assert dtos
    assert dtos[0].key == "gunHandgunT1Pistol"


@pytest.mark.timeout(1)
async def test_game_data_recipes_search_by_fuzzy_scores(
    loaded_recipes,
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.recipes.search_by_fuzzy(
            text="pistol",
            lang=LocalizationLanguage.ENGLISH,
        )

    for dto in dtos:
        assert 0 <= dto.trigram_score <= 1
        assert dto.fts_score >= 0
        assert dto.total_score >= 0


@pytest.mark.timeout(1)
async def test_game_data_recipes_search_by_fuzzy_returns_empty_list(
    loaded_recipes,
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.recipes.search_by_fuzzy(
            text="abracadabra123456",
            lang=LocalizationLanguage.ENGLISH,
        )

    assert dtos == []


@pytest.mark.timeout(1)
async def test_game_data_recipes_search_by_fuzzy_multilanguage(
    loaded_recipes,
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        english = await uow.recipes.search_by_fuzzy(
            text="pistol",
            lang=LocalizationLanguage.ENGLISH,
        )

        russian = await uow.recipes.search_by_fuzzy(
            text="пистолет",
            lang=LocalizationLanguage.RUSSIAN,
        )

    assert english
    assert russian
    assert english[0].key == russian[0].key


@pytest.mark.timeout(1)
async def test_game_data_recipes_search_by_fuzzy_sorted_by_score(
    loaded_recipes,
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.recipes.search_by_fuzzy(
            text="pistol",
            lang=LocalizationLanguage.ENGLISH,
        )

    scores = [dto.total_score for dto in dtos]

    assert scores == sorted(scores, reverse=True)


@pytest.mark.timeout(1)
async def test_game_data_recipes_search_by_fuzzy_typo(
    loaded_recipes,
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.recipes.search_by_fuzzy(
            text="pisotl",
            lang=LocalizationLanguage.ENGLISH,
        )

    assert dtos
    assert dtos[0].key == "gunHandgunT1Pistol"


@pytest.mark.timeout(1)
async def test_game_data_recipes_list_by_key_returns_results(
    loaded_recipes,
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.recipes.list_by_key(key="gunHandgunT1Pistol")

    assert dtos
    assert dtos[0].key == "gunHandgunT1Pistol"
