"""add_talent_last_logged_at_column

Revision ID: 944743c06eef
Revises: 899591a5f26d
Create Date: 2024-01-29 20:15:13.404220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = '944743c06eef'
down_revision: Union[str, None] = '899591a5f26d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('talent',
    sa.Column('last_logged_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')))

def downgrade() -> None:
    op.drop_column('talent','last_logged_at')
