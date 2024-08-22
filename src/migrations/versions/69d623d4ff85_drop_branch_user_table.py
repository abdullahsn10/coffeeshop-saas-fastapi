"""drop branch_user table

Revision ID: 69d623d4ff85
Revises: b9ede00dcff6
Create Date: 2024-08-21 23:28:32.211440

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "69d623d4ff85"
down_revision: Union[str, None] = "b9ede00dcff6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("branch_user")


def downgrade() -> None:
    op.create_table(
        "branch_user",
        sa.Column("branch_id", sa.Integer, nullable=False),
        sa.Column("manager_id", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("branch_id", "manager_id"),
        sa.ForeignKeyConstraint(["branch_id"], ["branch.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["manager_id"], ["user.id"], ondelete="RESTRICT"),
    )
