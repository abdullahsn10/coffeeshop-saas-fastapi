"""add coffee_shop_id column to inventory_item and menu_item tables

Revision ID: d86fa261070b
Revises: 69d623d4ff85
Create Date: 2024-08-21 23:30:23.655672

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d86fa261070b"
down_revision: Union[str, None] = "69d623d4ff85"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # remove the inventory_manager_id column from the inventory_item table
    op.drop_column("inventory_item", "inventory_manager_id")

    # add the coffee_shop_id column to the inventory_item table
    op.add_column(
        "inventory_item", sa.Column("coffee_shop_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        "fk_inventory_item_coffee_shop",
        "inventory_item",
        "coffee_shop",
        ["coffee_shop_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # add the coffee_shop_id column to the menu_item table
    op.add_column("menu_item", sa.Column("coffee_shop_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_menu_item_coffee_shop",
        "menu_item",
        "coffee_shop",
        ["coffee_shop_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    # remove the coffee_shop_id column and constraints from the inventory_item table
    op.drop_constraint(
        "fk_inventory_item_coffee_shop", "inventory_item", type_="foreignkey"
    )
    op.drop_column("inventory_item", "coffee_shop_id")

    # remove the coffee_shop_id column and constraints from the menu_item table
    op.drop_constraint("fk_menu_item_coffee_shop", "menu_item", type_="foreignkey")
    op.drop_column("menu_item", "coffee_shop_id")

    # add the inventory_manager_id column back to the inventory_item table
    op.add_column(
        "inventory_item", sa.Column("inventory_manager_id", sa.Integer(), nullable=True)
    )
