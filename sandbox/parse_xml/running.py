import json

from src.infrastructure.xml_parcer.common.parser import UniversalXmlParser
from src.infrastructure.xml_parcer.schemas import recipes


parser = UniversalXmlParser(
    file_path="C:/Steam/steamapps/common/7 Days To Die/Data/Config/recipes.xml",
    pattern=recipes.PATTERN,
)

final_data = parser.run()

schema = recipes.RecipeData.model_validate(final_data)


with open("final_data.json", "w", encoding="utf-8") as f:
    json.dump(schema.model_dump(), f, ensure_ascii=False, indent=4)
