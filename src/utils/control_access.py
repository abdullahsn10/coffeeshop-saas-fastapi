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
