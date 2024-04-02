"""tabla_talent_cache_normal

Revision ID: da5f10814af2
Revises: a13ac8efe4c7
Create Date: 2024-04-01 11:14:32.161451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = 'da5f10814af2'
down_revision: Union[str, None] = 'a13ac8efe4c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('talent_cache_normal',
    sa.PrimaryKeyConstraint('id','email_login'),
    sa.Column('id',sa.BigInteger()),
    sa.Column('email',sa.String(80),nullable=False),
    sa.Column('full_name',sa.String(80),nullable=False),
    sa.Column('profession',sa.String(80),nullable=False),
    sa.Column('rate',sa.BigInteger(),nullable=False),
    sa.Column('description',sa.String(860),nullable=False),
    sa.Column('github',sa.String(1000),nullable=False),
    sa.Column('linkedin',sa.String(1000),nullable=False),
    sa.Column('instagram',sa.String(1000),nullable=True),
    sa.Column('facebook',sa.String(1000),nullable=True),
    sa.Column('skills',sa.String(1000),nullable=False),
    sa.Column('categories',sa.String(1000),nullable=False),
    sa.Column('pagination',sa.BigInteger()),
    sa.Column('email_login',sa.String(80),nullable=False),

    )

def downgrade() -> None:
    op.drop_table('talent_cache_normal')
