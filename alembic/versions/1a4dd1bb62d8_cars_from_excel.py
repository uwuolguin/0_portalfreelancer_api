"""cars_from_excel

Revision ID: 1a4dd1bb62d8
Revises: daa7a7c580dd
Create Date: 2024-06-08 00:30:37.011288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a4dd1bb62d8'
down_revision: Union[str, None] = 'daa7a7c580dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('cars_from_excel',
    sa.PrimaryKeyConstraint('id'),
    sa.Column('id',sa.BigInteger(),autoincrement=True),
    sa.Column('brand',sa.String(1000),nullable=False),
    sa.Column('model',sa.String(1000),nullable=False),
    sa.Column('amount',sa.BigInteger(),nullable=False),
    sa.Column('lowest_price',sa.BigInteger(),nullable=False),
    sa.Column('highest_price',sa.BigInteger(),nullable=False),
    sa.Column('link',sa.String(1000),nullable=False),
    #,op.add_column('user',sa.Column('created_at2',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')))
    )

def downgrade() -> None:
    op.drop_table('cars_from_excel')