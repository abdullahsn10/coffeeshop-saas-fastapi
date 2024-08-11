from src.models import UserRole
from src import schemas
from src.helpers import user, coffee_shop, branch, branch_user
from src.exceptions.exception import *
from src.utils.hashing import Hash
from src.security.jwt import generate_token_for_user
from sqlalchemy.orm import Session


def signup(
    request: schemas.SignUpRequestBody, db: Session
) -> schemas.UserCredentialsInResponse:
    """
    This helper function used to signup a new coffee shop into the system,
    also create an admin user for the registered coffee shop.\n\n
    *Args:
        request (SignUpIn): The request object which contains shop_details and
        admin_details.\n

        db (Session): Database session object.\n
    *Returns:
        UserCredentialsInResponse: An object containing the registered admin user
        credentials(emai, phone_no).\n
    """
    coffee_shop_instance: schemas.CoffeeShopBase = request.shop_details
    branch_instance: schemas.BranchBase = request.branch_details
    admin_user_instance: schemas.UserBase = request.admin_details

    # check email or phone duplicates
    if user.is_user_exists_by_email(
        email=admin_user_instance.email, db=db
    ) or user.is_user_exists_by_phone(phone_no=admin_user_instance.phone_no, db=db):
        raise ShopsAppException(
            message="User with this email or phone number already exists.",
            status_code=400,
        )

    # create coffee shop, branch and admin
    created_coffee_shop = coffee_shop.create_coffee_shop(
        request=coffee_shop_instance, db=db
    )
    created_branch = branch.create_branch(
        request=branch_instance, db=db, coffee_shop_id=created_coffee_shop.id
    )
    created_admin_user = user.create_user(
        request=admin_user_instance,
        db=db,
        role=UserRole.ADMIN,
        branch_id=created_branch.id,
    )
    return schemas.UserCredentialsInResponse(
        email=created_admin_user.email,
        phone_no=created_admin_user.phone_no,
    )


def verify_user_credentials_and_gen_token(
    request: schemas.LoginRequestBody, db: Session
) -> schemas.Token:
    """
    This helper function used to verify a user's credentials and generate a
    JWT token for the user.\n
    *Args:
        request (LoginRequestBody): The request object which contains user_details\n
        db (Session): Database session object.\n
    *Returns:
        The JWT token for the user.\n
    """
    # get the user using the email
    current_user = user.get_user_by_email(db=db, email=request.username)

    if not current_user:
        raise ShopsAppException(message="Invalid Credentials", status_code=400)

    # verify password
    if not Hash.verify(
        plain_password=request.password, hashed_password=current_user.password
    ):
        raise ShopsAppException(
            message="Username or Password incorrect", status_code=400
        )

    # create jwt and return it
    # get the coffee shop id
    coffee_shop_id = branch.get_coffee_shop_id(db=db, branch_id=current_user.branch_id)
    access_token = generate_token_for_user(
        user=current_user, coffee_shop_id=coffee_shop_id
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
