import json

import src.application.game_data.schema
from src.infrastructure.xml_parcer.common.parser import UniversalXmlParser
from src.infrastructure.xml_parcer.patterns import recipes


parser = UniversalXmlParser(
    file_path="C:/Steam/steamapps/common/7 Days To Die/Data/Config/recipes.xml",
    pattern=recipes.PATTERN,
)

final_data = parser.run()

schema = src.application.game_data.schema.RecipesGameData.model_validate(final_data)


with open("final_data.json", "w", encoding="utf-8") as f:
    json.dump(schema.model_dump(), f, ensure_ascii=False, indent=4)
