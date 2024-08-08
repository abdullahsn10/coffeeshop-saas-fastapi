from sqlalchemy.orm import Session
from src import schemas, models
from src.utils.hashing import Hash
from src.exceptions.exception import *
from src.helpers import coffee_shop
from src.models.user import UserRole
from typing import Union


def is_exists_by_email(email: str, db: Session, excluded_user_id: int = None) -> bool:
    """
    This helper function used to check if a user exists by email.
    *Args:
        email (str): The email to check.
        db (Session): A database session.
        excluded_user_id (int): The user id to exclude from the check.
    *Returns:
        bool: True if the user exists, False otherwise.
    """
    if excluded_user_id is not None:
        return (
            db.query(models.User)
            .filter(models.User.email == email, models.User.id != excluded_user_id)
            .first()
            is not None
        )
    return db.query(models.User).filter(models.User.email == email).first() is not None


def is_exists_by_phone(
    phone_no: str, db: Session, excluded_user_id: int = None
) -> bool:
    """
    This helper function used to check if a user exists by phone number.
    *Args:
        phone_no (str): The email to check.
        db (Session): A database session.
        excluded_user_id (int): The user id to exclude from the check.
    *Returns:
        bool: True if the user exists, False otherwise.
    """
    if excluded_user_id is not None:
        return (
            db.query(models.User)
            .filter(
                models.User.phone_no == phone_no, models.User.id != excluded_user_id
            )
            .first()
            is not None
        )
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


def update(
    id: int,
    request: [schemas.UserPUTRequestBody, schemas.UserPATCHRequestBody],
    db: Session,
) -> models.User:
    """
    This helper function used to update a user.
    *Args:
        request (UserPUTRequestBody/ UserPATCHRequestBody): The user details to update.
        db (Session): A database session.
        user_id (int): The user id to update.
    *Returns:
        User: The updated user.
    """

    user_instance = find_by_id(user_id=id, db=db)
    if not user_instance:
        raise ShopsAppException(f"User with id {id} could not be found")

    # Update all fields of the user object based on the request
    update_data = request.model_dump(
        exclude_unset=True
    )  # Get dictionary of all set fields in request
    # hash the user password if it is updated
    if "password" in update_data:
        update_data["password"] = Hash.bcrypt_hash(password=update_data["password"])
    for field, value in update_data.items():
        setattr(user_instance, field, value)
    db.commit()
    db.refresh(user_instance)
    return user_instance


def validate_and_create_or_update(
    request: Union[schemas.UserPOSTRequestBody, schemas.UserPUTRequestBody],
    db: Session,
    admin_coffee_shop_id: int,
    creation: bool = True,
    user_id: int = None,
) -> schemas.UserCredentialsInResponse:
    """
    This helper function used to validate and create/update a new user.
    *Args:
        request (UserPOSTRequestBody/ UserPUTRequestBody): The user details to create or update.
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin who created/updated the user.
    *Returns:
        UserCredentialsInResponse: The created/updated user credentials.
    """

    # verify that the branch id belongs to the admin coffee shop
    if not coffee_shop.has_branch(
        id=admin_coffee_shop_id, branch_id=request.branch_id, db=db
    ):
        raise ShopsAppException("Branch does not belong to your coffee shop")

    if user_id is not None:
        # verify email and phone uniqueness and exclude the user to be updated
        # from the check (Update case)
        if is_exists_by_email(
            email=request.email, db=db, excluded_user_id=user_id
        ) or is_exists_by_phone(
            phone_no=request.phone_no, db=db, excluded_user_id=user_id
        ):
            raise ShopsAppAlreadyExistsException(
                "User with this email or phone number already exists"
            )
        # get the user role before updating
        before_update_user_role = find_by_id(user_id=user_id, db=db).role
    else:
        # verify email and phone uniqueness (Create case)
        if is_exists_by_email(email=request.email, db=db) or is_exists_by_phone(
            phone_no=request.phone_no, db=db
        ):
            raise ShopsAppAlreadyExistsException(
                "User with this email or phone number already exists"
            )
        before_update_user_role = None

    if creation:
        # create the user
        user_details = schemas.UserBase(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone_no=request.phone_no,
            password=request.password,
        )
        user_instance = create(
            request=user_details,
            role=request.role,
            branch_id=request.branch_id,
            db=db,
        )
    else:
        # update the user
        user_instance = update(request=request, db=db, id=user_id)
    # check if the created/updated user is admin, then attach all branches to
    # be managed by him
    # if the user is admin and the role was admin before updating, then do not
    # attach branches to him again
    if (
        user_instance.role == UserRole.ADMIN
        and before_update_user_role != UserRole.ADMIN
    ):
        coffee_shop.attach_all_branches_to_admin(
            id=admin_coffee_shop_id, manager_id=user_instance.id, db=db
        )

    return schemas.UserCredentialsInResponse(
        email=user_instance.email, phone_no=user_instance.phone_no
    )
