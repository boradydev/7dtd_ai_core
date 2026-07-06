from sqlalchemy import text

from src.infrastructure.db.postgres.repositories.common.sql_reader import sql_reader


class SQL:
    ADD_MANY = text(sql_reader("add_many.sql", __file__))
    CLEAR = text(sql_reader("clear.sql", __file__))
