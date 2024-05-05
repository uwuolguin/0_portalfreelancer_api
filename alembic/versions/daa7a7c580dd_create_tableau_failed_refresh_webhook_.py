"""create_tableau_failed_refresh_webhook_records

Revision ID: daa7a7c580dd
Revises: f8612933631d
Create Date: 2024-05-04 20:47:57.213588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = 'daa7a7c580dd'
down_revision: Union[str, None] = 'f8612933631d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table('tableau_failed_refreshed',
    sa.Column('tableau_url',sa.String(10000)),
    sa.Column('last_updated_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


    )


def downgrade() -> None:
    op.drop_table('tableau_failed_refreshed')
