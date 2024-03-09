"""drop_blacklistname

Revision ID: ec41c8c96211
Revises: b2ce0ef7c9a9
Create Date: 2024-01-30 20:57:18.865633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = 'ec41c8c96211'
down_revision: Union[str, None] = 'b2ce0ef7c9a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
 op.drop_table('blacklistname')


def downgrade() -> None:
    op.create_table('blacklistname',
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('full_name'),
    sa.Column('id',sa.BigInteger(),autoincrement=True),
    sa.Column('full_name',sa.String(80),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')),
    )
