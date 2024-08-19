from sqlalchemy.orm import Session
from src import schemas, models
from src.utils.hashing import Hash
from src.exceptions.exception import *
from src.helpers import coffee_shop, branch
from typing import Union
from fastapi import status


def is_user_exist(
    db: Session, email: str = None, phone_no: str = None, excluded_user_id: int = None
) -> bool:
    """
    This helper function used to check if a user exists by email or phone
    *Args:
        email (str): The email to check.
        phone_no (str) : The phone number of the user to check
        db (Session): A database session.
        excluded_user_id (int): The user id to exclude from the check.
    *Returns:
        bool: True if the user exists, False otherwise.
    """
    query = db.query(models.User)

    if email:
        query = query.filter(models.User.email == email)
    if phone_no:
        query = query.filter(models.User.phone_no == phone_no)
    if excluded_user_id:
        query = query.filter(models.User.id != excluded_user_id)

    return query.first() is not None


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


def find_user(
    db: Session,
    user_id: int = None,
    phone_no: str = None,
    email: str = None,
    coffee_shop_id: int = None,
    exclude_deleted: bool = True,
    raise_exc: bool = True,
) -> models.User:
    """
    This helper function used to get a user by id, coffee_shop_id, ..etc
    *Args:
        user_id (int): The user id.
        phone (str): The phone number of the user.
        email (str): The email of the user.
        db (Session): A database session.
        coffee_shop_id (int): optional argument, if it's provided then this means to put it in the query also
        exclude_deleted (bool): optional argument, default True, if it's True then the query will exclude the deleted users
        raise_exc (bool): optional argument, default True, if it's True then the function will raise an exception if the user not found
    *Returns:
        the User instance if exists, None otherwise.
    """
    query = db.query(models.User)

    if user_id:
        query = query.filter(models.User.id == user_id)
    elif phone_no:
        query = query.filter(models.User.phone_no == phone_no)
    elif email:
        query = query.filter(models.User.email == email)
    else:
        raise Exception("You must provide either user_id, phone_no, or email")

    if coffee_shop_id:
        query = query.join(models.Branch).filter(
            models.Branch.coffee_shop_id == coffee_shop_id
        )

    if exclude_deleted:
        query = query.filter(models.User.deleted == False)
    found_user = query.first()
    if raise_exc and not found_user:
        raise ShopsAppException(
            message=f"This user does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return found_user


def find_all_users(db: Session, coffee_shop_id: int = None) -> list[models.User]:
    """
    This helper function used to get all users in a specific coffee shop.
    *Args:
        db (Session): A database session.
        coffee_shop_id (int): The coffee shop id.
    *Returns:
        list[User]: The list of all users.
    """
    query = db.query(models.User).filter(models.User.deleted == False)
    if coffee_shop_id:
        query = query.join(models.Branch).filter(
            models.Branch.coffee_shop_id == coffee_shop_id
        )
    return query.all()


def update_user(
    request: Union[schemas.UserPUTRequestBody, schemas.UserPATCHRequestBody],
    db: Session,
    user_instance: models.User,
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
    found_branch = branch.find_branch(
        db=db,
        branch_id=branch_id,
        coffee_shop_id=admin_coffee_shop_id,
        raise_exc=False,
    )
    if not found_branch:
        raise ShopsAppException(
            message=f"Branch with id={branch_id} does not exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if is_user_exist(
        email=user_email,
        db=db,
        excluded_user_id=updated_user_id,
    ) or is_user_exist(phone_no=user_phone_no, db=db, excluded_user_id=updated_user_id):
        raise ShopsAppException(
            message="User with this email or phone number already exists",
            status_code=status.HTTP_409_CONFLICT,  # conflict error
        )


def validate_and_create_user(
    request: schemas.UserPOSTRequestBody,
    db: Session,
    admin_coffee_shop_id: int,
) -> schemas.UserPOSTResponse:
    """
    This helper function used to validate and create a new user.
    *Args:
        request (UserPOSTRequestBody): The user details to create
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin who created the user.
    *Returns:
        UserPOSTResponse: The created user details.
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

    return schemas.UserPOSTResponse(
        id=created_user.id,
        first_name=created_user.first_name,
        last_name=created_user.last_name,
        email=created_user.email,
        phone_no=created_user.phone_no,
        role=created_user.role,
        branch_id=created_user.branch_id,
    )


def full_update_user(
    request: schemas.UserPUTRequestBody,
    db: Session,
    admin_coffee_shop_id: int,
    user_id: int,
) -> schemas.UserPUTAndPATCHResponse:
    """
    This helper function used to validate and update user.
    *Args:
        request (UserPUTRequestBody): The user details to update
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin who updated the user.
        user_id (int): the id of the user needed to be updated
    *Returns:
        UserPUTAndPATCHResponse: The updated user details.
    """

    user_instance = find_user(
        user_id=user_id, db=db, coffee_shop_id=admin_coffee_shop_id
    )

    validate_user_on_create_update(
        admin_coffee_shop_id=admin_coffee_shop_id,
        branch_id=request.branch_id,
        user_email=request.email,
        user_phone_no=request.phone_no,
        db=db,
        updated_user_id=user_id,
    )
    # update the user
    updated_user = update_user(request=request, db=db, user_instance=user_instance)

    return schemas.UserPUTAndPATCHResponse(
        id=updated_user.id,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        email=updated_user.email,
        phone_no=updated_user.phone_no,
        role=updated_user.role,
        branch_id=updated_user.branch_id,
    )


def partial_update_user(
    request: schemas.UserPATCHRequestBody,
    db: Session,
    admin_coffee_shop_id: int,
    creation: bool = True,
    user_id: int = None,
) -> schemas.UserPUTAndPATCHResponse:
    """
    This helper function used to validate and partially update a new user.
    *Args:
        request (UserPATCHRequestBody): The user details to partially update.
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin who updated the user.
    *Returns:
        UserPUTAndPATCHResponse: The updated user credentials.
    """
    user_instance = find_user(
        user_id=user_id, db=db, coffee_shop_id=admin_coffee_shop_id
    )

    if request.branch_id:
        # verify that the branch id belongs to the admin coffee shop
        found_branch = branch.find_branch(
            db=db,
            branch_id=request.branch_id,
            coffee_shop_id=admin_coffee_shop_id,
            raise_exc=False,
        )
        if not found_branch:
            raise ShopsAppException(
                message=f"Branch with id={request.branch_id} does not exist",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    # verify email and phone uniqueness and exclude the user to be updated
    # from the check
    if request.phone_no:
        if is_user_exist(phone_no=request.phone_no, db=db, excluded_user_id=user_id):
            raise ShopsAppException(
                message="User with this email or phone already exists",
                status_code=status.HTTP_409_CONFLICT,
            )
    if request.email:
        if is_user_exist(email=request.email, db=db, excluded_user_id=user_id):
            raise ShopsAppException(
                message="User with this email or phone already exists",
                status_code=status.HTTP_409_CONFLICT,
            )
    # update the user
    updated_user = update_user(request=request, db=db, user_instance=user_instance)

    return schemas.UserPUTAndPATCHResponse(
        id=updated_user.id,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        email=updated_user.email,
        phone_no=updated_user.phone_no,
        role=updated_user.role,
        branch_id=updated_user.branch_id,
    )


def delete_user(user_id: int, db: Session, admin_coffee_shop_id: int) -> None:
    """
    This helper function used to delete a user by id.
    *Args:
        user_id (int): The user id.
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin that the use must belongs to
    """
    user_instance = find_user(
        user_id=user_id, db=db, coffee_shop_id=admin_coffee_shop_id
    )
    user_instance.deleted = True
    db.commit()
    db.refresh(user_instance)


def validate_user_on_restore(
    db: Session,
    branch_id: int,
    coffee_shop_id: int,
    phone_no: str = None,
    email: str = None,
) -> models.User:
    """
    This helper function used to validate the user on restore, check if this
    user already exists or not, check the branch to restore, ...etc
    *Args:
        phone_no (str): The phone number of the user to restore
        email (str): The email of the user to restore
        branch_id (int): The branch id to restore the user to
        coffee_shop_id (int): The coffee shop id of the admin who restore the user
    *Returns:
        raise Exceptions in case of violation, return the restored_user otherwise
    """

    # check if the user belongs to the admin coffee shop
    if phone_no:
        restored_user = find_user(
            phone_no=phone_no,
            db=db,
            coffee_shop_id=coffee_shop_id,
            exclude_deleted=False,
        )

    elif email:
        restored_user = find_user(
            email=email,
            db=db,
            coffee_shop_id=coffee_shop_id,
            exclude_deleted=False,
        )
    else:
        raise ShopsAppException(
            message="Email or phone number must be provided",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # check if the provided branch belongs to the admin coffee shop
    found_branch = branch.find_branch(
        db=db, branch_id=branch_id, coffee_shop_id=coffee_shop_id
    )

    if not found_branch:
        raise ShopsAppException(
            message=f"Branch with id={branch_id} does not exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # check if the user deleted
    if not restored_user.deleted:
        raise ShopsAppException(
            message="User already exists in a branch",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return restored_user


def restore_deleted_user(
    db: Session,
    request: schemas.UserInRestorePATCHRequestBody,
    admin_coffee_shop_id: int,
) -> schemas.UserPUTAndPATCHResponse:
    """
    This helper function used to restore a deleted user to a branch by his/her phone
    or email.
    *Args:
        db (Session): A database session.
        request (schemas.UserInRestorePATCHRequestBody): The user details to restore
        admin_coffee_shop_id (int): the coffee shop id of the admin need to restore the user
    *Returns:
        UserPUTAndPATCHResponse: The restored user details.
    """
    restored_user = validate_user_on_restore(
        phone_no=request.phone_no,
        email=request.email,
        db=db,
        branch_id=request.branch_id,
        coffee_shop_id=admin_coffee_shop_id,
    )
    restored_user.deleted = False
    restored_user.branch_id = request.branch_id
    db.commit()
    db.refresh(restored_user)
    return schemas.UserPUTAndPATCHResponse(
        id=restored_user.id,
        first_name=restored_user.first_name,
        last_name=restored_user.last_name,
        email=restored_user.email,
        phone_no=restored_user.phone_no,
        role=restored_user.role,
        branch_id=restored_user.branch_id,
    )
