from sqlalchemy.orm import Session
from src.exceptions.exception import *
from src.helpers import user, coffee_shop, inventory_item, menu_item
from fastapi import status


def check_if_user_can_access_shop(user_coffee_shop_id: int, target_coffee_shop_id: int):
    """
    This utils function performs a logic that checks if a user can make
    changes on a specific coffee shop.
    *Args:
        user_coffee_shop_id (int): The id of the user's coffee shop.
        target_coffee_shop_id (int): The id of the target coffee shop that
        the user wants to make changes on.
    *Returns:
        raise a ShopAppException if the user cannot make changes on the
        coffee shop.
    """
    if user_coffee_shop_id != target_coffee_shop_id:
        raise ShopsAppException(
            message="You are not authorized to make changes on this shop",
            status_code=status.HTTP_401_UNAUTHORIZED,  # unauthorized error
        )


def check_if_user_belongs_to_this_coffee_shop(
    user_id: int, coffee_shop_id: int, db: Session
):
    """
    This utils function performs a logic that checks if a user belongs to a specific
    coffee shop.
    *Args:
        user_id (int): The id of the user.
        coffee_shop_id (int): The id of the coffee shop.
        db (Session): A database session.
    *Returns:
        raise a ShopAppException if the user does not belong to the
        coffee shop.
    """
    user_instance = user.find_user_by_id(user_id=user_id, db=db)
    if not user_instance or not coffee_shop.is_shop_has_this_branch(
        coffee_shop_id=coffee_shop_id, branch_id=user_instance.branch_id, db=db
    ):
        raise ShopsAppException(
            message="You are not authorized to show or make changes on this user",
            status_code=status.HTTP_401_UNAUTHORIZED,  # un authorized exception
        )


def check_if_user_can_access_this_item(
    item_id: int, db: Session, admin_coffee_shop_id: int, is_inventory_item: bool = True
):
    """
    This utils function performs a logic that checks if a user can make changes on
    an item either inventory item or menu item.
    *Args:
    item_id (int): The id of the item.
    db (Session): A database session.
    admin_coffee_shop_id (int): The coffee shop id of the admin who needs to make changes on the item.
    *Returns:
        raise a ShopAppException if the user is not authorized to make changes
    """
    if is_inventory_item:
        found_inventory_item = inventory_item.find_inventory_item_by_id(
            db=db, inventory_item_id=item_id
        )
        if (
            not found_inventory_item
            or found_inventory_item.coffee_shop_id != admin_coffee_shop_id
        ):
            raise ShopsAppException(
                message="You are not authorized to show or make changes on this item",
                status_code=status.HTTP_401_UNAUTHORIZED,  # un authorized exception
            )
    else:
        pass
