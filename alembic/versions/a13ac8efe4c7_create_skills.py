"""create_skills

Revision ID: a13ac8efe4c7
Revises: c869582e2b36
Create Date: 2024-03-06 13:19:04.176263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a13ac8efe4c7'
down_revision: Union[str, None] = 'c869582e2b36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('skills',
    sa.PrimaryKeyConstraint('skill'),
    sa.Column('skill',sa.String(1000),nullable=False))


def downgrade() -> None:
    op.drop_table('skills')