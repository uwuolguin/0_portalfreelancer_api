"""create_categories

Revision ID: c869582e2b36
Revises: 29513cd8673b
Create Date: 2024-03-06 12:49:56.331205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c869582e2b36'
down_revision: Union[str, None] = '29513cd8673b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('categories',
    sa.PrimaryKeyConstraint('category'),
    sa.Column('category',sa.String(1000),nullable=False)
    )

def downgrade() -> None:
    op.drop_table('categories')
