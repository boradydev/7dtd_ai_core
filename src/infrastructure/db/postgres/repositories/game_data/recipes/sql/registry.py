from sqlalchemy import TextClause, text

from src.application.game_data.common.localization.languages import LocalizationConfig
from src.infrastructure.db.postgres.repositories.common.sql_reader import sql_reader
from src.infrastructure.db.postgres.repositories.game_data.common.sql.registry import (
    CommonSQL,
)


class SQL(CommonSQL):
    ADD_MANY = text(sql_reader("add_many.sql", __file__))
    CLEAR = text(sql_reader("clear.sql", __file__))

    @classmethod
    def GET_SEARCH_BY_FUZZY(cls, config: LocalizationConfig) -> TextClause:
        sql = cls._SEARCH_BY_FUZZY
        sql = sql.replace("'__SEARCH_LANG__'", f"'{config.lang}'")
        sql = sql.replace("l.__SEARCH_COLUMN__", f"l.{config.column}")
        return text(sql)
