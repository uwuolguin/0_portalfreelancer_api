"""complaints

Revision ID: e1cab0677055
Revises: 92e58d219a5d
Create Date: 2024-01-19 21:11:38.135368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = 'e1cab0677055'
down_revision: Union[str, None] = '92e58d219a5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('complaints',
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.Column('id',sa.BigInteger(),autoincrement=True),
    sa.Column('email',sa.String(80),nullable=False),
    sa.Column('email_sent',sa.String(1000),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')),

    #,op.add_column('user',sa.Column('created_at2',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')))

    )
def downgrade() -> None:
    op.drop_table('complaints')
