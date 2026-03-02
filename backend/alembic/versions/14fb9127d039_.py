"""empty message

Revision ID: 14fb9127d039
Revises: 02312349030b, 39f852208f4a
Create Date: 2026-02-23 13:31:58.663723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14fb9127d039'
down_revision: Union[str, Sequence[str], None] = ('02312349030b', '39f852208f4a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
