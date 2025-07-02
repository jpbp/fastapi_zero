"""fix updated_at default value

Revision ID: a757bd9be833
Revises: 3a5ba60a4dd0
Create Date: 2025-06-30 14:12:09.632055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a757bd9be833'
down_revision: Union[str, Sequence[str], None] = '3a5ba60a4dd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
