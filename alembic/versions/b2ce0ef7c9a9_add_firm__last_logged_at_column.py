"""add_firm__last_logged_at_column

Revision ID: b2ce0ef7c9a9
Revises: 944743c06eef
Create Date: 2024-01-29 20:30:04.759221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = 'b2ce0ef7c9a9'
down_revision: Union[str, None] = '944743c06eef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('firm',
    sa.Column('last_logged_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')))

def downgrade() -> None:
    op.drop_column('firm','last_logged_at')