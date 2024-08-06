from shops_app.models import UserRole
from shops_app.schemas.authentication import SignUpIn
from shops_app.schemas.user import UserBase, UserCredentialsInResponse
from shops_app.schemas.coffee_shop import CoffeeShopBase
from shops_app.schemas.response import ResponseMessage
from shops_app.helpers import user, coffee_shop
from shops_app.exceptions.exception import *

from sqlalchemy.orm import Session


def signup(request: SignUpIn, db: Session) -> UserCredentialsInResponse:
    """
    This helper function used to signup a new coffee shop into the system,
    also create an admin user for the registered coffee shop.
    *Args:
        request (SignUpIn): The request object which contains shop_details and
        admin_details.

        db (Session): Database session object.
    *Returns:
        UserCredentialsInResponse: An object containing the registered admin user
        credentials(emai, phone_no).
    """
    coffee_shop_instance: CoffeeShopBase = request.shop_details
    admin_user_instance: UserBase = request.admin_details

    # check email or phone duplicates
    if (user.is_exists_by_email(email=admin_user_instance.email, db=db) or
            user.is_exists_by_phone(phone_no=admin_user_instance.phone_no, db=db)):
        raise ShopsAppException('User with this email or phone number already exists.')

    # create coffee shop and admin
    created_coffee_shop = coffee_shop.create(request=coffee_shop_instance, db=db)
    created_admin_user = user.create(request=admin_user_instance, db=db,
                                     role=UserRole.ADMIN)
    return UserCredentialsInResponse(
            email=created_admin_user.email,
            phone_no=created_admin_user.phone_no,
        )
