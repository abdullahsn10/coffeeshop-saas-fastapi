from sqlalchemy.orm import Session
from src.exceptions.exception import *
from src.helpers import user, coffee_shop
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
        raise a ShopAppUnAuthorizedException if the user cannot make changes on the
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
        raise a ShopAppUnAuthorizedException if the user does not belong to the
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
