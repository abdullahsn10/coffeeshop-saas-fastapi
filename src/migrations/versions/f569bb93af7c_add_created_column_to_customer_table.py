"""add created column to customer table

Revision ID: f569bb93af7c
Revises: ad3d5b97d40c
Create Date: 2024-08-21 23:38:48.080773

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f569bb93af7c"
down_revision: Union[str, None] = "ad3d5b97d40c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # add the created column to the customer table with a default value of CURRENT_TIMESTAMP
    op.add_column(
        "customer", sa.Column("created", sa.TIMESTAMP(), server_default=sa.func.now())
    )


def downgrade():
    # remove the created column from the customer table
    op.drop_column("customer", "created")
