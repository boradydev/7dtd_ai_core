import json

import src.app.game_data.schemas.recipes
from src.infra.xml_parser.common.parser import UniversalXmlParser
from src.infra.xml_parser.patterns import recipes


parser = UniversalXmlParser(
    file_path="C:/Steam/steamapps/common/7 Days To Die/Data/Config/recipes.xml",
    pattern=recipes.PATTERN,
)

final_data = parser.run()

schema = src.application.game_data.schemas.recipes.RecipesGameData.model_validate(final_data)


with open("final_data.json", "w", encoding="utf-8") as f:
    json.dump(schema.model_dump(), f, ensure_ascii=False, indent=4)
