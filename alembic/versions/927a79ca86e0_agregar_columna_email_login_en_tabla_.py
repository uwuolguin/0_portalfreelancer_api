"""agregar_columna_email_login_en_tabla_cache_talent_normal

Revision ID: 927a79ca86e0
Revises: da5f10814af2
Create Date: 2024-04-01 14:40:45.179346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = '927a79ca86e0'
down_revision: Union[str, None] = 'da5f10814af2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('talent_cache_normal',
    sa.Column('email_login',sa.String(80),nullable=False))

def downgrade() -> None:
    op.drop_column('talent_cache_normal','email_login')