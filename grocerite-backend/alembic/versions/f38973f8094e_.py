"""empty message

Revision ID: f38973f8094e
Revises: 71abe667f2f8
Create Date: 2024-05-04 17:33:35.396029

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f38973f8094e'
down_revision: Union[str, None] = '71abe667f2f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
