"""create task

Revision ID: 0.1
Revises: 
Create Date: 2025-08-17 10:33:30.665008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0.1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True,
                  nullable=False),
        sa.Column("update", sa.JSON(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("task")
