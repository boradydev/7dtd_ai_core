import pytest

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
async def test_game_data_recipes_list_by_key_returns_results(
    loaded_recipes,
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.recipes.list_by_key(key="gunHandgunT1Pistol")

    assert dtos
    assert dtos[0].key == "gunHandgunT1Pistol"
