from sqlalchemy import text

from src.infra.db.postgres.repos.common.sql_reader import sql_reader


class SQL:
    SAVE = text(sql_reader("save.sql", __file__))
    FIND_BY_PLAYER_ID = text(sql_reader("find_by_player_id.sql", __file__))
