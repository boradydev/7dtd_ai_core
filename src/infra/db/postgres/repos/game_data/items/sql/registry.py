from sqlalchemy import TextClause, text

from src.app.game_data.common.localization.languages import LocalizationConfig
from src.infra.db.postgres.repos.common.sql_reader import sql_reader
from src.infra.db.postgres.repos.game_data.common.sql.registry import (
    CommonSQL,
)


class SQL(CommonSQL):
    @classmethod
    def get_search_by_fuzzy(cls, config: LocalizationConfig) -> TextClause:
        sql = cls._SEARCH_BY_FUZZY
        sql = sql.replace("'__SEARCH_LANG__'", f"'{config.lang}'")
        sql = sql.replace("l.__SEARCH_COLUMN__", f"l.{config.column}")
        return text(sql)
