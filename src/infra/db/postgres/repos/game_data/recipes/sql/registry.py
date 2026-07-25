from sqlalchemy import text

from src.infra.db.postgres.repos.common.sql_reader import sql_reader
from src.infra.db.postgres.repos.game_data.common.sql.registry import (
    CommonSQL,
)


class SQL(CommonSQL):
    ADD_MANY = text(sql_reader("add_many.sql", __file__))
    CLEAR = text(sql_reader("clear.sql", __file__))
    LIST_BY_KEY = text(sql_reader("list_by_key.sql", __file__))
