from shops_app.models import UserRole
from shops_app import schemas
from shops_app.helpers import user, coffee_shop
from shops_app.exceptions.exception import *
from shops_app.utils.hashing import Hash
from sqlalchemy.orm import Session


def signup(request: schemas.SignUpIn, db: Session) -> schemas.UserCredentialsInResponse:
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
    coffee_shop_instance: schemas.CoffeeShopBase = request.shop_details
    admin_user_instance: schemas.UserBase = request.admin_details

    # check email or phone duplicates
    if (user.is_exists_by_email(email=admin_user_instance.email, db=db) or
            user.is_exists_by_phone(phone_no=admin_user_instance.phone_no, db=db)):
        raise ShopsAppException('User with this email or phone number already exists.')

    # create coffee shop and admin
    created_coffee_shop = coffee_shop.create(request=coffee_shop_instance, db=db)
    created_admin_user = user.create(request=admin_user_instance, db=db,
                                     role=UserRole.ADMIN)
    return schemas.UserCredentialsInResponse(
        email=created_admin_user.email,
        phone_no=created_admin_user.phone_no,
    )


def verify_user_credentials_and_gen_token(request: schemas.LoginIn, db: Session) -> schemas.Token:
    # get the user using the email
    current_user = user.get_by_email(db=db, email=request.username)

    if not current_user:
        raise ShopsAppException('Invalid Credentials')

    # verify password
    if not Hash.verify(plain_password=request.password,
                       hashed_password=current_user.password):
        raise ShopsAppException('Username or Password incorrect')

    # create jwt and return it
    # access_token = generate_token_for_user(current_user)
    return schemas.Token(access_token="blablabla", token_type="bearer")
