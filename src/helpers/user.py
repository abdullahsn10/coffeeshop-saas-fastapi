from sqlalchemy.orm import Session
from src import schemas, models
from src.utils.hashing import Hash
from src.exceptions.exception import *
from src.helpers import coffee_shop
from src.models.user import UserRole


def is_exists_by_email(email: str, db: Session) -> bool:
    """
    This helper function used to check if a user exists by email.
    *Args:
        email (str): The email to check.
    *Returns:
        bool: True if the user exists, False otherwise.
    """
    return db.query(models.User).filter(models.User.email == email).first() is not None


def is_exists_by_phone(phone_no: str, db: Session) -> bool:
    """
    This helper function used to check if a user exists by phone number.
    *Args:
        phone_no (str): The email to check.
    *Returns:
        bool: True if the user exists, False otherwise.
    """
    return (
        db.query(models.User).filter(models.User.phone_no == phone_no).first()
        is not None
    )


def create(
    request: schemas.UserBase, role: models.UserRole, branch_id: int, db: Session
) -> models.User:
    """
    This helper function used to create a new user.
    *Args:
        request (UserBase): The user to create.
        role (UserRole): The role of the user to create.
        db (Session): A database session.
    *Returns:
        User: The created user.
    """
    # hash the user password
    request.password = Hash.bcrypt_hash(password=request.password)

    created_user_instance = models.User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone_no=request.phone_no,
        password=request.password,
        role=role,
        branch_id=branch_id,
    )
    db.add(created_user_instance)
    db.commit()
    db.refresh(created_user_instance)
    return created_user_instance


def find_by_id(user_id: int, db: Session) -> models.User:
    """
    This helper function used to get a user by id.
    *Args:
        user_id (int): The user id.
        db (Session): A database session.
    *Returns:
        the User instance if exists, None otherwise.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_branch_id(user_id: int, db: Session) -> int:
    """
    This helper function used to get the branch id of the user.
    *Args:
        user_id (int): The user id.
        db (Session): A database session.
    *Returns:
        the branch id of the user
    """
    user = find_by_id(user_id=user_id, db=db)
    return user.branch_id


def get_by_email(email: str, db: Session) -> models.User:
    """
    This helper function used to get a user by email.
    *Args:
        email (str): The email to check.
        db (Session): A database session.

    *Returns:
        the User instance if exists, None otherwise.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_coffee_shop_id(db: Session, user_id: int) -> int:
    """
    This helper function will be used to get the coffee shop id of the user
    *Args:
        db (Session): A database session.
        user_id (int): The user id.
    *Returns:
        the coffee shop id of the user
    """
    # join query to get coffee shop id
    result = (
        db.query(models.CoffeeShop.id)
        .filter(models.User.id == user_id)
        .filter(models.User.branch_id == models.Branch.id)
        .filter(models.Branch.coffee_shop_id == models.CoffeeShop.id)
        .first()
    )
    return result[0]


def validate_and_create(
    request: schemas.UserPOSTRequestBody, db: Session, admin_coffee_shop_id: int
) -> schemas.UserCredentialsInResponse:
    """
    This helper function used to validate and create a new user.
    *Args:
        request (UserPOSTRequestBody): The user to create.
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin who created the user.
    *Returns:
        UserPOSTResponseBody: The created user.
    """

    # verify that the branch id belongs to the admin coffee shop
    if not coffee_shop.has_branch(
        id=admin_coffee_shop_id, branch_id=request.branch_id, db=db
    ):
        raise ShopsAppException("Branch does not belong to your coffee shop")

    # verify email and phone uniqueness
    if is_exists_by_email(email=request.email, db=db) or is_exists_by_phone(
        phone_no=request.phone_no, db=db
    ):
        raise ShopsAppAlreadyExistsException(
            "User with this email or phone number already exists"
        )

    # create the user
    user_details = schemas.UserBase(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone_no=request.phone_no,
        password=request.password,
    )
    created_user = create(
        request=user_details,
        role=request.role,
        branch_id=request.branch_id,
        db=db,
    )
    # check if the created user is admin, then attach all branches to
    # be managed by him
    if request.role == UserRole.ADMIN:
        coffee_shop.attach_all_branches_to_admin(
            id=admin_coffee_shop_id, manager_id=created_user.id, db=db
        )

    return schemas.UserCredentialsInResponse(
        email=created_user.email, phone_no=created_user.phone_no
    )
