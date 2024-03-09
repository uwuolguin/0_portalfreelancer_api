"""login_attempt

Revision ID: 29513cd8673b
Revises: ff16966db105
Create Date: 2024-02-29 23:05:03.795033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = '29513cd8673b'
down_revision: Union[str, None] = 'ff16966db105'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('loginAttempt',
    sa.PrimaryKeyConstraint('id'),
    sa.Column('id',sa.BigInteger(),autoincrement=True),
    sa.Column('email',sa.String(80),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')),
    )

def downgrade() -> None:
    op.drop_table('loginAttempt')
