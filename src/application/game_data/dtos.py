from dataclasses import dataclass
from typing import Any


@dataclass
class RecipeDTO:
    name: str
    raw_data: dict[str, Any]
