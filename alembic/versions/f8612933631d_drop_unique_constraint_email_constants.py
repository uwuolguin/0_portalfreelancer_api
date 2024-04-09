"""drop_unique_constraint_email_constants

Revision ID: f8612933631d
Revises: a13ac8efe4c7
Create Date: 2024-04-09 15:15:03.742065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8612933631d'
down_revision: Union[str, None] = 'a13ac8efe4c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("complaints_email_key", "complaints")


def downgrade() -> None:
    op.create_unique_constraint('complaints_email_key', 'complaints', ['email'])
