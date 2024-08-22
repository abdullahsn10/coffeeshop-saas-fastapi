"""new updates

Revision ID: dab05b4a193b
Revises: 1f6c3ad293cf
Create Date: 2024-08-22 09:16:12.846879

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "dab05b4a193b"
down_revision: Union[str, None] = "1f6c3ad293cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "order",
        "status",
        existing_type=postgresql.ENUM(
            "PENDING", "IN_PROGRESS", "COMPLETED", "CLOSED", name="orderstatus"
        ),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "order",
        "status",
        existing_type=postgresql.ENUM(
            "PENDING", "IN_PROGRESS", "COMPLETED", "CLOSED", name="orderstatus"
        ),
        nullable=True,
    )
    # ### end Alembic commands ###