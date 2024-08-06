from sqlalchemy.orm import Session
from shops_app import schemas, models
from shops_app.utils.hashing import Hash


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


def create(request: schemas.UserBase, role: models.UserRole, db: Session) -> models.User:
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

    # *******NOTE: branch id
    created_user_instance = models.User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone_no=request.phone_no,
        password=request.password,
        role=role,
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
