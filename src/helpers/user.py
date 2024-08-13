from sqlalchemy.orm import Session
from src import schemas, models
from src.utils.hashing import Hash
from src.exceptions.exception import *
from src.helpers import coffee_shop
from typing import Union
from fastapi import status


def is_user_exists_by_email(
    email: str, db: Session, excluded_user_id: int = None
) -> bool:
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


def is_user_exists_by_phone(
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


def create_user(
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


def find_user_by_id(
    user_id: int, db: Session, coffee_shop_id: int = None
) -> models.User:
    """
    This helper function used to get a user by id.
    *Args:
        user_id (int): The user id.
        db (Session): A database session.
        coffee_shop_id (int): optional argument, if it's provided then this means to put it in the query also
    *Returns:
        the User instance if exists, None otherwise.
    """
    if not coffee_shop_id:
        return (
            db.query(models.User)
            .filter(models.User.id == user_id, models.User.deleted == False)
            .first()
        )
    return (
        db.query(models.User)
        .filter(
            models.User.id == user_id,
            models.User.branch_id == models.Branch.id,
            models.Branch.coffee_shop_id == coffee_shop_id,
        )
        .first()
    )


def find_all_users_in_this_shop(coffee_shop_id: int, db: Session) -> list[models.User]:
    """
    This helper function used to get all users in a specific coffee shop.
    *Args:
        db (Session): A database session.
        coffee_shop_id (int): The coffee shop id.
    *Returns:
        list[User]: The list of all users.
    """
    return (
        db.query(models.User)
        .filter(
            models.User.branch_id == models.Branch.id,
            models.Branch.coffee_shop_id == coffee_shop_id,
            models.User.deleted == False,
        )
        .all()
    )


def get_branch_id_of_user(user_id: int, db: Session) -> int:
    """
    This helper function used to get the branch id of the user.
    *Args:
        user_id (int): The user id.
        db (Session): A database session.
    *Returns:
        the branch id of the user
    """
    user = find_user_by_id(user_id=user_id, db=db)
    return user.branch_id


def get_user_by_email(email: str, db: Session) -> models.User:
    """
    This helper function used to get a user by email.
    *Args:
        email (str): The email to check.
        db (Session): A database session.

    *Returns:
        the User instance if exists, None otherwise.
    """
    return (
        db.query(models.User)
        .filter(models.User.email == email, models.User.deleted == False)
        .first()
    )


def get_coffee_shop_id_of_user(db: Session, user_id: int) -> int:
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


def update_user(
    user_id: int,
    request: Union[schemas.UserPUTRequestBody, schemas.UserPATCHRequestBody],
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

    user_instance = find_user_by_id(user_id=user_id, db=db)
    if not user_instance:
        raise ShopsAppException(
            message=f"User with id {user_id} could not be found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

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


def validate_user_on_create_update(
    admin_coffee_shop_id: int,
    branch_id: int,
    user_email: str,
    user_phone_no: str,
    db: Session,
    updated_user_id: int = None,
) -> None:
    """
    This helper function will be used to apply validation logic on creation or
    update, validation will include:
        - validate that the admin's coffee shop has the branch that exists in
        the request body
        - validate the user's email uniqueness
        - validate the user's phone number uniqueness
    *Args:
        - admin_coffee_shop_id (int): The coffee shop id of the admin who create/update the user.
        - branch_id (int): The branch id that exists in the request body.
        - user_email (str): The created/updated user email.
        - user_phone_no(str): The created/updated user phone number.
        - db (Session): A database session.
    *Returns:
        raise Exceptions in case of violation, pass otherwise
    """

    # verify that the branch id belongs to the admin coffee shop
    if not coffee_shop.is_shop_has_this_branch(
        coffee_shop_id=admin_coffee_shop_id, branch_id=branch_id, db=db
    ):
        raise ShopsAppException(
            message=f"Branch with id={branch_id} does not exist in your coffee shop",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if updated_user_id is not None:
        # verify email and phone uniqueness and exclude the user to be updated
        # from the check (Update case)
        if is_user_exists_by_email(
            email=user_email, db=db, excluded_user_id=updated_user_id
        ) or is_user_exists_by_phone(
            phone_no=user_phone_no, db=db, excluded_user_id=updated_user_id
        ):
            raise ShopsAppException(
                message="User with this email or phone number already exists",
                status_code=status.HTTP_409_CONFLICT,  # conflict error
            )
    else:
        # verify email and phone uniqueness (Create case)
        if is_user_exists_by_email(email=user_email, db=db) or is_user_exists_by_phone(
            phone_no=user_phone_no, db=db
        ):
            raise ShopsAppException(
                message="User with this email or phone number already exists",
                status_code=status.HTTP_409_CONFLICT,  # conflict error
            )


def validate_and_create_user(
    request: schemas.UserPOSTRequestBody,
    db: Session,
    admin_coffee_shop_id: int,
) -> schemas.UserCredentialsInResponse:
    """
    This helper function used to validate and createa new user.
    *Args:
        request (UserPOSTRequestBody): The user details to create
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin who created the user.
    *Returns:
        UserCredentialsInResponse: The created user credentials.
    """

    validate_user_on_create_update(
        admin_coffee_shop_id=admin_coffee_shop_id,
        branch_id=request.branch_id,
        user_email=request.email,
        user_phone_no=request.phone_no,
        db=db,
    )
    # create the user
    user_details = schemas.UserBase(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone_no=request.phone_no,
        password=request.password,
    )
    created_user = create_user(
        request=user_details,
        role=request.role,
        branch_id=request.branch_id,
        db=db,
    )

    return schemas.UserCredentialsInResponse(
        email=created_user.email, phone_no=created_user.phone_no
    )


def full_update_user(
    request: schemas.UserPUTRequestBody,
    db: Session,
    admin_coffee_shop_id: int,
    user_id: int,
) -> schemas.UserCredentialsInResponse:
    """
    This helper function used to validate and update user.
    *Args:
        request (UserPUTRequestBody): The user details to update
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin who updated the user.
        user_id (int): the id of the user needed to be updated
    *Returns:
        UserCredentialsInResponse: The created user credentials.
    """

    validate_user_on_create_update(
        admin_coffee_shop_id=admin_coffee_shop_id,
        branch_id=request.branch_id,
        user_email=request.email,
        user_phone_no=request.phone_no,
        db=db,
        updated_user_id=user_id,
    )
    # update the user
    updated_user = update_user(request=request, db=db, user_id=user_id)

    return schemas.UserCredentialsInResponse(
        email=updated_user.email, phone_no=updated_user.phone_no
    )


def partial_update_user(
    request: schemas.UserPATCHRequestBody,
    db: Session,
    admin_coffee_shop_id: int,
    creation: bool = True,
    user_id: int = None,
) -> schemas.UserCredentialsInResponse:
    """
    This helper function used to validate and partially update a new user.
    *Args:
        request (UserPATCHRequestBody): The user details to partially update.
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin who updated the user.
    *Returns:
        UserCredentialsInResponse: The updated user credentials.
    """
    if request.branch_id:
        # verify that the branch id belongs to the admin coffee shop
        if not coffee_shop.is_shop_has_this_branch(
            coffee_shop_id=admin_coffee_shop_id, branch_id=request.branch_id, db=db
        ):
            raise ShopsAppException(
                message="Branch does not belong to your coffee shop",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    # verify email and phone uniqueness and exclude the user to be updated
    # from the check
    if request.phone_no:
        if is_user_exists_by_phone(
            phone_no=request.phone_no, db=db, excluded_user_id=user_id
        ):
            raise ShopsAppException(
                message="User with this phone number already exists",
                status_code=status.HTTP_409_CONFLICT,
            )
    if request.email:
        if is_user_exists_by_email(
            email=request.email, db=db, excluded_user_id=user_id
        ):
            raise ShopsAppException(
                message="User with this phone number already exists",
                status_code=status.HTTP_409_CONFLICT,
            )
    # update the user
    user_instance = update_user(request=request, db=db, user_id=user_id)

    return schemas.UserCredentialsInResponse(
        email=user_instance.email, phone_no=user_instance.phone_no
    )


def delete_user_by_id(user_id: int, db: Session, admin_coffee_shop_id: int) -> None:
    """
    This helper function used to delete a user by id.
    *Args:
        user_id (int): The user id.
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin that the use must belongs to
    """
    user_instance = find_user_by_id(
        user_id=user_id, db=db, coffee_shop_id=admin_coffee_shop_id
    )
    if not user_instance:
        raise ShopsAppException(
            message="You are not authorized to show or make changes on this user",
            status_code=status.HTTP_401_UNAUTHORIZED,  # un authorized exception
        )
    user_instance.deleted = True
    db.commit()
    db.refresh(user_instance)


def restore_deleted_user_to_a_branch(
    db: Session,
    request: schemas.UserInRestorePATCHRequestBody,
    admin_coffee_shop_id: int,
):
    """
    This helper function used to restore a deleted user to a branch by his/her phone
    or email.
    *Args:
        db (Session): A database session.
        request (schemas.UserInRestorePATCHRequestBody): The user details to restore
        admin_coffee_shop_id (int): the coffee shop id of the admin need to restore the user
    """

    # check if the user belongs to the user coffee shop
    if request.phone_no:
        restored_user = coffee_shop.get_user_in_the_shop_by_phone(
            user_phone_no=request.phone_no, db=db, coffee_shop_id=admin_coffee_shop_id
        )

    elif request.email:
        restored_user = coffee_shop.get_user_in_the_shop_by_email(
            user_email=request.email, db=db, coffee_shop_id=admin_coffee_shop_id
        )
    else:
        raise ShopsAppException(
            message="Email or phone number must be provided",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not restored_user:
        raise ShopsAppException(
            message="You are not authorized to make changes on this user",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # check if the provided branch belongs to the admin's coffee shop
    if not coffee_shop.is_shop_has_this_branch(
        coffee_shop_id=admin_coffee_shop_id, branch_id=request.branch_id, db=db
    ):
        raise ShopsAppException(
            message="You are not authorized to make changes on this branch",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # check if the user deleted
    if not restored_user.deleted:
        raise ShopsAppException(
            message="User already exists in a branch",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    restored_user.deleted = False
    restored_user.branch_id = request.branch_id
    db.commit()
    db.refresh(restored_user)
    return restored_user
