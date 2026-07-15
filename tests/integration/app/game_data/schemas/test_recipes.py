from src.app.game_data.schemas.recipes import RecipesGameData
from src.infra.xml_parser.common.parser import UniversalXmlParser
from src.infra.xml_parser.patterns.recipes import PATTERN


def test_recipes(config_dir):
    xml_parser = UniversalXmlParser(
        config_dir / "recipes.xml",
        PATTERN,
    )
    raw_data = xml_parser.run()

    schemas = RecipesGameData.model_validate(raw_data)

    assert len(schemas.recipes) == len(raw_data["recipes"])
