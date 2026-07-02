from pydantic import BaseModel, field_validator


PATTERN = {
    "recipes": {
        "$xml_tag": "recipe",
        "$pattern": [
            {
                "item_name": {"$xml_attr": "name"},
                "output_count": {"$xml_attr": "count"},
                "craft_station": {"$xml_attr": "craft_area"},
                "required_ingredients": {
                    "$xml_tag": "ingredient",
                    "$pattern": [
                        {
                            "name": {"$xml_attr": "name"},
                            "quantity": {"$xml_attr": "count"},
                        }
                    ],
                },
            }
        ],
    }
}


class Ingredient(BaseModel):
    name: str
    quantity: int

    @field_validator("quantity", mode="before")
    @classmethod
    def quantity_to_int(cls, value):
        return int(value)


class Recipe(BaseModel):
    item_name: str
    output_count: int
    craft_station: str
    required_ingredients: list[Ingredient]

    @field_validator("output_count", mode="before")
    @classmethod
    def output_count_to_int(cls, value):
        return int(value)

    @field_validator("craft_station", mode="before")
    @classmethod
    def replace_none_with_backpack(cls, value):
        if value is None:
            return "backpack"
        return value


class RecipeData(BaseModel):
    recipes: list[Recipe]
