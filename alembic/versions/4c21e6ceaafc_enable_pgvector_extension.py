"""enable pgvector extension

Revision ID: 4c21e6ceaafc
Revises: 3b5dffa72288
Create Date: 2026-08-16 19:30:49.136654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c21e6ceaafc'
down_revision: Union[str, Sequence[str], None] = '3b5dffa72288'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Enable the PostgreSQL vector extension."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    """Disable the PostgreSQL vector extension."""
    op.execute("DROP EXTENSION IF EXISTS vector")
