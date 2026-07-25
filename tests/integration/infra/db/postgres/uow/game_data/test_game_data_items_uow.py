import pytest

from src.app.game_data.common.localization.languages import LocalizationLanguage
from src.app.game_data.dtos import MatchedItemDTO
from src.infra.db.postgres.uow.game_data import GameDataUOW


@pytest.mark.timeout(1)
async def test_game_data_items_search_by_fuzzy_returns_results(
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.items.search_by_fuzzy(
            text="pistol",
            lang=LocalizationLanguage.ENGLISH,
        )

    assert dtos
    assert dtos[0].key == "gunHandgunT1Pistol"


@pytest.mark.timeout(1)
async def test_game_data_items_search_by_fuzzy_scores(
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.items.search_by_fuzzy(
            text="pistol",
            lang=LocalizationLanguage.ENGLISH,
        )

    for dto in dtos:
        assert 0 <= dto.trigram_score <= 1
        assert dto.fts_score >= 0
        assert dto.total_score >= 0


@pytest.mark.timeout(1)
async def test_game_data_items_search_by_fuzzy_returns_empty_list(
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.items.search_by_fuzzy(
            text="abracadabra123456",
            lang=LocalizationLanguage.ENGLISH,
        )

    assert dtos == []


@pytest.mark.timeout(1)
async def test_game_data_items_search_by_fuzzy_multilanguage(
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        english = await uow.items.search_by_fuzzy(
            text="pistol",
            lang=LocalizationLanguage.ENGLISH,
        )

        russian = await uow.items.search_by_fuzzy(
            text="пистолет",
            lang=LocalizationLanguage.RUSSIAN,
        )

    assert english
    assert russian
    assert english[0].key == russian[0].key


@pytest.mark.timeout(1)
async def test_game_data_items_search_by_fuzzy_sorted_by_score(
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.items.search_by_fuzzy(
            text="pistol",
            lang=LocalizationLanguage.ENGLISH,
        )

    scores = [dto.total_score for dto in dtos]

    assert scores == sorted(scores, reverse=True)


@pytest.mark.timeout(1)
async def test_game_data_items_search_by_fuzzy_typo(
    game_data_uow,
) -> None:
    async with game_data_uow as uow:
        dtos = await uow.items.search_by_fuzzy(
            text="pisotl",
            lang=LocalizationLanguage.ENGLISH,
        )

    assert dtos
    assert dtos[0].key == "gunHandgunT1Pistol"
