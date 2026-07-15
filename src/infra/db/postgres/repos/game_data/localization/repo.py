from sqlalchemy.ext.asyncio import AsyncSession

from src.app.game_data.abcs import ILocalizationRepository
from src.app.game_data.schemas.localization import LocalizationGameData
from src.infra.db.postgres.repos.game_data.localization.sql.registry import (
    SQL,
)


class LocalizationRepository(ILocalizationRepository):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def add_many(
        self,
        dtos: list[LocalizationGameData],
    ) -> None:
        params = []
        for dto in dtos:
            params.append(
                dict(
                    key=dto.key,
                    file=dto.file,
                    type=dto.type,
                    used_in_main_menu=dto.used_in_main_menu,
                    no_translate=dto.no_translate,
                    keep_loaded=dto.keep_loaded,
                    english=dto.english,
                    context=dto.context,
                    german=dto.german,
                    spanish=dto.spanish,
                    french=dto.french,
                    italian=dto.italian,
                    japanese=dto.japanese,
                    koreana=dto.koreana,
                    polish=dto.polish,
                    brazilian=dto.brazilian,
                    russian=dto.russian,
                    turkish=dto.turkish,
                    schinese=dto.schinese,
                    tchinese=dto.tchinese,
                )
            )
        await self._session.execute(SQL.ADD_MANY, params)

    async def clear(self) -> None:
        await self._session.execute(SQL.CLEAR)
