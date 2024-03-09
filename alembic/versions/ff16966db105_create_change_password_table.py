"""create_change_password_table

Revision ID: ff16966db105
Revises: ec41c8c96211
Create Date: 2024-02-24 01:46:55.798747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = 'ff16966db105'
down_revision: Union[str, None] = 'ec41c8c96211'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('changepassword',
    sa.PrimaryKeyConstraint('id'),
    sa.Column('id',sa.BigInteger(),autoincrement=True),
    sa.Column('email',sa.String(80),nullable=False),
    sa.Column('password',sa.String(1000),nullable=True),
    sa.Column('origin',sa.String(80),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    #,op.add_column('user',sa.Column('created_at2',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')))

    )


def downgrade() -> None:
    op.drop_table('changepassword')
