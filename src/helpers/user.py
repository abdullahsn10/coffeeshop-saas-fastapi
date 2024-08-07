from sqlalchemy.orm import Session
from src import schemas, models
from src.utils.hashing import Hash


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
    return db.query(models.User).filter(models.User.phone_no == phone_no).first() is not None


def create(request: schemas.UserBase, role: models.UserRole, branch_id: int,
           db: Session) -> models.User:
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
        branch_id=branch_id
    )
    db.add(created_user_instance)
    db.commit()
    db.refresh(created_user_instance)
    return created_user_instance


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
    :param db: db session
    :param user_id: the user id to get the coffee shop id for
    :return: the coffee shop id
    """
    result = (db.query(models.CoffeeShop.id)
              .filter(models.User.id == user_id)
              .filter(models.User.branch_id == models.Branch.id)
              .filter(models.Branch.coffee_shop_id == models.CoffeeShop.id)
              .first())
    return result[0]
