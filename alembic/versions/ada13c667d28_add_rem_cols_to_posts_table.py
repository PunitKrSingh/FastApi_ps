"""add rem cols to posts table

Revision ID: ada13c667d28
Revises: d6a46e255b0f
Create Date: 2023-12-21 12:42:17.763184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ada13c667d28'
down_revision: Union[str, None] = 'd6a46e255b0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('is_published',sa.Boolean(),nullable=False,server_default='True')
                  )
    op.add_column('posts',
                  sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text
                            ('NOW()'))
                  )
    pass


def downgrade() -> None:
    op.drop_column('posts','is_published')
    op.drop_column('posts','created_at')

    pass
