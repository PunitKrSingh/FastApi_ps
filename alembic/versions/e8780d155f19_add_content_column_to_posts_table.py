"""add content column to posts table

Revision ID: e8780d155f19
Revises: 7d0323545308
Create Date: 2023-12-21 12:16:05.726004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8780d155f19'
down_revision: Union[str, None] = '7d0323545308'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
