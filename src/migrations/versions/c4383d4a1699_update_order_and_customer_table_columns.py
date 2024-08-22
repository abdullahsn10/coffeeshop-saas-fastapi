"""update order and customer table columns

Revision ID: c4383d4a1699
Revises: d86fa261070b
Create Date: 2024-08-21 23:33:23.655677

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c4383d4a1699"
down_revision: Union[str, None] = "d86fa261070b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define the Enum type
order_status_enum = sa.Enum(
    "PENDING", "IN_PROGRESS", "COMPLETED", "CLOSED", name="order_status"
)


def upgrade():
    # add assigner_id column to the order table
    op.add_column("order", sa.Column("assigner_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_order_assigner",
        "order",
        "user",
        ["assigner_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # aAdd status column to the order table
    op.add_column("order", sa.Column("status", sa.String(length=50)))

    # rename employee_id column to issuer_id
    op.alter_column("order", "employee_id", new_column_name="issuer_id")

    # create the enum type
    order_status_enum.create(op.get_bind())

    # use enum in status column
    op.execute(
        """
        ALTER TABLE "order"
        ALTER COLUMN status TYPE order_status
        USING status::order_status;
    """
    )

    # add coffee_shop_id column to the customer table
    op.add_column("customer", sa.Column("coffee_shop_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_customer_coffee_shop",
        "customer",
        "coffee_shop",
        ["coffee_shop_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # drop the unique constraint from the customer phone no
    op.drop_constraint("customer_phone_no_key", "customer", type_="unique")

    # add unique constraint on a combination of phone_no with coffee_shop_id
    op.create_unique_constraint(
        "unique_phone_shop", "customer", ["phone_no", "coffee_shop_id"]
    )


def downgrade():
    # drop the unique constraint on phone_no and coffee_shop_id
    op.drop_constraint("unique_phone_shop", "customer", type_="unique")

    # add the unique constraint back to phone_no
    op.create_unique_constraint("customer_phone_no_key", "customer", ["phone_no"])

    # drop the coffee_shop_id column and foreign key constraint from the customer table
    op.drop_constraint("fk_customer_coffee_shop", "customer", type_="foreignkey")
    op.drop_column("customer", "coffee_shop_id")

    # revert status column to VARCHAR(50)
    op.alter_column(
        "order", "status", type_=sa.String(length=50), existing_type=order_status_enum
    )

    # drop the enum type
    order_status_enum.drop(op.get_bind())

    # rename issuer_id column back to employee_id
    op.alter_column("order", "issuer_id", new_column_name="employee_id")

    # drop the assigner_id column and foreign key constraint from the order table
    op.drop_constraint("fk_order_assigner", "order", type_="foreignkey")
    op.drop_column("order", "assigner_id")
