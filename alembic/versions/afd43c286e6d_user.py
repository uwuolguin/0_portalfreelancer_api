"""user

Revision ID: afd43c286e6d
Revises: 
Create Date: 2024-01-18 12:05:06.515273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = 'afd43c286e6d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('talent',
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.Column('id',sa.BigInteger(),autoincrement=True),
    sa.Column('email',sa.String(80),nullable=False),
    sa.Column('password',sa.String(1000),nullable=False),
    sa.Column('picture_directory',sa.String(10000),nullable=False,server_default='directory'),
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
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')),
    sa.Column('last_updated_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    #,op.add_column('user',sa.Column('created_at2',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')))


    )


def downgrade() -> None:
    op.drop_table('talent')
    #,op.drop_column('users','created_at2')