from pydantic import BaseModel, field_validator


class Ingredient(BaseModel):
    name: str
    quantity: int

    @field_validator("quantity", mode="before")
    @classmethod
    def quantity_to_int(cls, value):
        return int(value)


class RecipeGameData(BaseModel):
    name: str
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

    @property
    def raw_data(self):
        return self.model_dump()


class RecipesGameData(BaseModel):
    recipes: list[RecipeGameData]
