"""contacts

Revision ID: 0afae1b26bff
Revises: c09e13f96338
Create Date: 2024-01-19 20:32:14.129654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = '0afae1b26bff'
down_revision: Union[str, None] = 'c09e13f96338'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('contacts',
    sa.Column('talent_id',sa.BigInteger(),nullable=False),
    sa.Column('firm_id',sa.BigInteger(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')),
    #,op.add_column('user',sa.Column('created_at2',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')))
#lo comentado es un ejemplo de como agregra una revision para añadir y sacar columnas
    )

    op.create_foreign_key('talent_fk',source_table="contacts",referent_table="talent",
                          local_cols=['talent_id'],remote_cols=['id'],ondelete="CASCADE"

    )

    op.create_foreign_key('firm_fk',source_table="contacts",referent_table="firm",
                          local_cols=['firm_id'],remote_cols=['id'],ondelete="CASCADE"

    )

    op.create_primary_key('pk_contacts','contacts',['talent_id','firm_id','created_at'])

    pass


def downgrade() -> None:
    op.drop_table('contacts')
    #,op.drop_column('users','created_at2')
    pass
