from abc import ABC

from src.infra.db.postgres.alembic.migrations.sql_reader import sql_reader


class CommonSQL(ABC):
    _SEARCH_BY_FUZZY = sql_reader("search_by_fuzzy.sql", __file__)
