"""create task is_processed

Revision ID: 0.2
Revises: 0.1
Create Date: 2025-08-17 10:55:09.445766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0.2'
down_revision: Union[str, Sequence[str], None] = '0.1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE task ADD COLUMN is_processed BOOLEAN NOT NULL DEFAULT FALSE
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE task DROP COLUMN is_processed
        """
    )
