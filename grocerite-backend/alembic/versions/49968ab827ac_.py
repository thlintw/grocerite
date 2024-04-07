"""empty message

Revision ID: 49968ab827ac
Revises: 7b7bd563afb2
Create Date: 2024-04-07 11:04:30.023992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49968ab827ac'
down_revision: Union[str, None] = '7b7bd563afb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
