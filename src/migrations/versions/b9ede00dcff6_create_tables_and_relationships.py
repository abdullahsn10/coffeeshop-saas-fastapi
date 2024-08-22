"""Create tables and relationships

Revision ID: b9ede00dcff6
Revises: 
Create Date: 2024-08-21 23:00:41.855716

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b9ede00dcff6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # create 'coffee_shop' table
    op.create_table(
        "coffee_shop",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("location", sa.String(255), nullable=False),
        sa.Column("contact_info", sa.String(255)),
    )

    # create 'branch' table
    op.create_table(
        "branch",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("location", sa.String(255), nullable=False),
        sa.Column("deleted", sa.Boolean, server_default="FALSE"),
        sa.Column("coffee_shop_id", sa.Integer),
        sa.ForeignKeyConstraint(
            ["coffee_shop_id"], ["coffee_shop.id"], ondelete="RESTRICT"
        ),
    )

    # create 'user' table
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(255), nullable=False),
        sa.Column("last_name", sa.String(255), nullable=False),
        sa.Column("phone_no", sa.String(255), nullable=False, unique=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column(
            "role",
            sa.Enum("CASHIER", "CHEF", "ORDER_RECEIVER", "ADMIN", name="user_role"),
            nullable=False,
        ),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("deleted", sa.Boolean, server_default="FALSE"),
        sa.Column("branch_id", sa.Integer),
        sa.ForeignKeyConstraint(["branch_id"], ["branch.id"], ondelete="RESTRICT"),
    )

    # create 'branch_user' table (relationship table)
    op.create_table(
        "branch_user",
        sa.Column("branch_id", sa.Integer, nullable=False),
        sa.Column("manager_id", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("branch_id", "manager_id"),
        sa.ForeignKeyConstraint(["branch_id"], ["branch.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["manager_id"], ["user.id"], ondelete="RESTRICT"),
    )

    # create 'inventory_item' table
    op.create_table(
        "inventory_item",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("expire_date", sa.Date),
        sa.Column("prod_date", sa.Date),
        sa.Column("available_quantity", sa.Integer, nullable=False),
        sa.Column("deleted", sa.Boolean, server_default="FALSE"),
        sa.Column("inventory_manager_id", sa.Integer),
        sa.ForeignKeyConstraint(
            ["inventory_manager_id"], ["user.id"], ondelete="RESTRICT"
        ),
    )

    # create 'menu_item' table
    op.create_table(
        "menu_item",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.String(255)),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("deleted", sa.Boolean, server_default="FALSE"),
    )

    # create 'customer' table
    op.create_table(
        "customer",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("deleted", sa.Boolean, server_default="FALSE"),
        sa.Column("phone_no", sa.String(20), nullable=False, unique=True),
    )

    # create 'order' table
    op.create_table(
        "order",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "issue_date",
            sa.TIMESTAMP,
            server_default=sa.func.current_timestamp(),
            nullable=False,
        ),
        sa.Column("customer_id", sa.Integer),
        sa.Column("employee_id", sa.Integer),
        sa.ForeignKeyConstraint(["customer_id"], ["customer.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["employee_id"], ["user.id"], ondelete="RESTRICT"),
    )

    # create 'order_item' table
    op.create_table(
        "order_item",
        sa.Column("order_id", sa.Integer, nullable=False),
        sa.Column("item_id", sa.Integer, nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("order_id", "item_id"),
        sa.ForeignKeyConstraint(["order_id"], ["order.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["item_id"], ["menu_item.id"], ondelete="RESTRICT"),
    )


def downgrade() -> None:
    # drop the 'order_item' table
    op.drop_table("order_item")

    # drop the 'order' table
    op.drop_table("order")

    # drop the 'customer' table
    op.drop_table("customer")

    # drop the 'menu_item' table
    op.drop_table("menu_item")

    # drop the 'inventory_item' table
    op.drop_table("inventory_item")

    # drop the 'branch_user' table
    op.drop_table("branch_user")

    # drop the 'user' table
    op.drop_table("user")

    # drop the 'branch' table
    op.drop_table("branch")

    # drop the 'coffee_shop' table
    op.drop_table("coffee_shop")

    # drop the 'user_role' ENUM type
    op.execute("DROP TYPE user_role")
