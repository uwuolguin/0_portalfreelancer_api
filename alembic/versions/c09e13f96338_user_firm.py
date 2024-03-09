"""user_firm

Revision ID: c09e13f96338
Revises: afd43c286e6d
Create Date: 2024-01-19 20:06:10.539892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = 'c09e13f96338'
down_revision: Union[str, None] = 'afd43c286e6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('firm',
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.Column('id',sa.BigInteger(),autoincrement=True),
    sa.Column('email',sa.String(80),nullable=False),
    sa.Column('password',sa.String(1000),nullable=False),
    sa.Column('full_name',sa.String(80),nullable=False),
    sa.Column('contact_email',sa.String(80),nullable=False),
    sa.Column('contact_phone',sa.String(80),nullable=False),
    sa.Column('email_template_to_send',sa.String(860),nullable=False),
    sa.Column('linkedin',sa.String(1000),nullable=False),
    sa.Column('instagram',sa.String(1000),nullable=True),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')),
    sa.Column('last_updated_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    #,op.add_column('user',sa.Column('created_at2',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')))

    )


def downgrade() -> None:
    op.drop_table('firm')
