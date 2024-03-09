"""blacklistwords

Revision ID: 899591a5f26d
Revises: cb12ad4c243e
Create Date: 2024-01-29 00:22:04.649875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '899591a5f26d'
down_revision: Union[str, None] = 'cb12ad4c243e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('blacklistwords',
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('words'),
    sa.Column('id',sa.BigInteger(),autoincrement=True),
    sa.Column('words',sa.String(80),nullable=False),

    #,op.add_column('user',sa.Column('created_at2',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')))

    )

def downgrade() -> None:
    op.drop_table('blacklistwords')
