from dataclasses import dataclass
from typing import Any


@dataclass
class RecipeDTO:
    key: str
    raw_data: dict[str, Any]

@dataclass
class MatchedItemDTO:
    key: str
    name: str
    fts_score: float
    trigram_score: float
    total_score: float