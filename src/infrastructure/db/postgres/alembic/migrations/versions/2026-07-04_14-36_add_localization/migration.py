"""empty message

Revision ID: 54123c66ccc9
Revises: ee3abe05b87d
Create Date: 2026-07-04 14:36:00.037596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54123c66ccc9'
down_revision: Union[str, Sequence[str], None] = 'ee3abe05b87d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(sql_reader("upgrade.sql", __file__))


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sql_reader("downgrade.sql", __file__))
