"""
empty message.

Revision ID: ee3abe05b87d
Revises: e7dc382495aa
Create Date: 2026-07-02 14:38:25.108211

"""

from collections.abc import Sequence

from alembic import op

from src.infra.db.postgres.alembic.migrations.sql_reader import sql_reader


# revision identifiers, used by Alembic.
revision: str = "ee3abe05b87d"
down_revision: str | Sequence[str] | None = "e7dc382495aa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(sql_reader("upgrade.sql", __file__))


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sql_reader("downgrade.sql", __file__))
