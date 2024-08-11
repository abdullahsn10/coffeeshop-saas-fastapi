from typing import Dict
from src import schemas, models
from sqlalchemy.orm import Session
from src.exceptions.exception import *
from src.helpers import coffee_shop


def create_branch(
    request: schemas.BranchBase, coffee_shop_id: int, db: Session
) -> models.Branch:
    """
    This helper function will be used to create a new branch
    *Args:
        request (schemas.BranchBase): schema instance that contains branch details
        db (Session): database session
        coffee_shop_id (int): id of the coffee shop to create the branch in
    *Returns:
        the created branch
    """
    # check if the shop exists
    if not coffee_shop.find_coffee_shop_by_id(db=db, coffee_shop_id=coffee_shop_id):
        raise ShopsAppException(
            message=f"Coffe Shop with id = {coffee_shop_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    created_branch = models.Branch(
        name=request.name, location=request.location, coffee_shop_id=coffee_shop_id
    )
    db.add(created_branch)
    db.commit()
    db.refresh(created_branch)
    return created_branch


def get_coffee_shop_id(branch_id: int, db: Session) -> int:
    """
    This helper function will be used to get the coffee shop id from the branch id
    *Args:
        branch_id (int): branch id
        db (Session): database session
    *Returns:
        coffee shop id
    """
    branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    return branch.coffee_shop_id


def get_all_users_in_branch(branch_id: int, db: Session) -> list[models.User]:
    """
    This helper function will be used to get all users in a branch
    *Args:
        branch_id (int): branch id
        db (Session): database session
    *Returns:
        list of users in the branch
    """
    return db.query(models.User).filter(models.User.branch_id == branch_id).all()


def is_branch_have_users(branch_id: int, db: Session) -> bool:
    """
    This helper function will be used to check if a branch has users
    *Args:
        branch_id (int): branch id
        db (Session): database session
    *Returns:
        True if the branch has users, False otherwise
    """
    return (
        db.query(models.User)
        .filter(models.User.branch_id == branch_id, models.User.deleted == False)
        .first()
        is not None
    )


def find_branch_in_this_coffee_shop(
    branch_id: int, db: Session, coffee_shop_id: int
) -> models.Branch:
    """
    This helper will be used to find a branch by id and coffee shop id
    in otherwords, it will check if the branch belongs to the shop
    *Args:
        branch_id (int): branch id to be found
        db (Session): database session
        coffee_shop_id (int): coffee shop id that the branch belongs to
    *Returns:
        the found branch
    """

    return (
        db.query(models.Branch)
        .filter(
            models.Branch.id == branch_id,
            models.Branch.deleted == False,
            models.Branch.coffee_shop_id == coffee_shop_id,
        )
        .first()
    )


def update_branch(
    request: schemas.BranchBase, db: Session, branch_id: int, coffee_shop_id: int
) -> models.Branch:
    """
    This helper function will be used to update a branch
    *Args:
        request (schemas.BranchBase): schema instance that contains branch details
        db (Session): database session
        branch_id (int): branch id
        coffee_shop_id (int): coffee shop id
        user_coffee_shop_id (int): user coffee shop id
    *Returns:
        the updated branch
    """

    # check if the branch belongs to this coffee shop
    found_branch = find_branch_in_this_coffee_shop(
        db=db, branch_id=branch_id, coffee_shop_id=coffee_shop_id
    )
    if not found_branch:
        raise ShopsAppException(
            message=f"Branch with id = {branch_id} does not exist in this coffee shop",
            status_code=status.HTTP_404_NOT_FOUND,  # not found error
        )

    # Update all fields of the branch object based on the request
    update_data = request.model_dump(
        exclude_unset=True
    )  # Get dictionary of all set fields in request
    for field, value in update_data.items():
        setattr(found_branch, field, value)
    db.commit()
    db.refresh(found_branch)
    return found_branch


def delete_branch_by_id(db: Session, branch_id: int, coffee_shop_id: int) -> None:
    """
    This helper function will be used to delete a branch
    *Args:
        db (Session): database session
        branch_id (int): branch id to delete
        coffee_shop_id (int): coffee shop id
        user_coffee_shop_id (int): user coffee shop id
    *Returns:
        a dict representation of the deleted branch
    """

    # check if the branch belongs to this coffee shop
    found_branch = find_branch_in_this_coffee_shop(
        db=db, branch_id=branch_id, coffee_shop_id=coffee_shop_id
    )
    if not found_branch:
        raise ShopsAppException(
            message=f"Branch with id = {branch_id} does not exist in this coffee shop",
            status_code=status.HTTP_404_NOT_FOUND,  # not found error
        )

    # check if the branch has users
    if is_branch_have_users(branch_id=branch_id, db=db):
        raise ShopsAppException(
            message="Branch has associated users, please remove them first",
            status_code=status.HTTP_409_CONFLICT,  # conflict error
        )
    found_branch.deleted = True
    db.commit()
