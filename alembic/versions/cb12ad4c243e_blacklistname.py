"""blacklistname

Revision ID: cb12ad4c243e
Revises: 9d0f80d3c120
Create Date: 2024-01-29 00:13:34.429311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = 'cb12ad4c243e'
down_revision: Union[str, None] = '9d0f80d3c120'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('blacklistname',
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('full_name'),
    sa.Column('id',sa.BigInteger(),autoincrement=True),
    sa.Column('full_name',sa.String(80),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')),

    #,op.add_column('user',sa.Column('created_at2',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')))

    )

def downgrade() -> None:
    op.drop_table('blacklistname')