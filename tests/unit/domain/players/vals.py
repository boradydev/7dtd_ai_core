import pytest

from src.domain.players import excs
from src.domain.players.vals import PlayerId


class TestPlayerIdValidation:
    """Группа тестов для валидации идентификатора игрока (PlayerId)."""

    def test_success_creation_with_valid_steamid64(self) -> None:
        valid_id = "76561198004196286"
        player_id = PlayerId(valid_id)
        assert player_id.value == "76561198004196286"

    @pytest.mark.parametrize(
        "invalid_id",
        [
            "",  # Пустая строка
            "7656119",  # Только префикс (слишком короткий)
            "7656119800419628",  # 16 цифр (не хватает одной)
            "765611980041962866",  # 18 цифр (одна лишняя)
            "7656119abc4196286",  # Буквы вместо цифр в теле ID
            "STEAM_0:0:2098143",  # Старый текстовый формат SteamID2
            "[U:1:4196286]",  # Формат SteamID3
            "76561198004196286 ",  # Валидный ID, но с пробелом на конце
        ],
    )
    def test_raise_exception_when_steamid_format_is_invalid(
        self, invalid_id: str
    ) -> None:
        with pytest.raises(excs.InvalidPlayerIdException):
            PlayerId(invalid_id)

    def test_player_id_is_frozen(self) -> None:
        """Проверяет, что Value Object защищен от мутаций после создания."""
        player_id = PlayerId("76561198004196286")

        with pytest.raises(AttributeError):
            player_id.value = "76561190000000000"  # type: ignore
