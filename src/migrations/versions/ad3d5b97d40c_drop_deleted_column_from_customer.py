"""drop deleted column from customer

Revision ID: ad3d5b97d40c
Revises: c4383d4a1699
Create Date: 2024-08-21 23:37:30.126913

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ad3d5b97d40c"
down_revision: Union[str, None] = "c4383d4a1699"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # drop the deleted column from the customer table
    op.drop_column("customer", "deleted")


def downgrade():
    # readd the deleted column to the customer table
    op.add_column("customer", sa.Column("deleted", sa.Boolean(), nullable=True))
