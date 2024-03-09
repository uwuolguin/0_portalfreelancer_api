"""blacklistemail

Revision ID: 9d0f80d3c120
Revises: e1cab0677055
Create Date: 2024-01-28 23:48:15.420033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = '9d0f80d3c120'
down_revision: Union[str, None] = 'e1cab0677055'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('blacklistemail',
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.Column('id',sa.BigInteger(),autoincrement=True),
    sa.Column('email',sa.String(80),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')),

    #,op.add_column('user',sa.Column('created_at2',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')))

    )

def downgrade() -> None:
    op.drop_table('blacklistemail')
