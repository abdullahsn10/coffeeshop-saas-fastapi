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
            message=f"Coffee shop with this id ={target_coffee_shop_id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND,  # unauthorized error
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
    user_instance = user.find_user_by_id(
        user_id=user_id, db=db, coffee_shop_id=coffee_shop_id
    )
    if not user_instance:
        raise ShopsAppException(
            message=f"This user with id = {user_id} does not exist in the coffee shop",
            status_code=status.HTTP_404_NOT_FOUND,  # un authorized exception
        )
