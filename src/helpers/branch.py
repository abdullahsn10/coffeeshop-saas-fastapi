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
    found_shop = coffee_shop.find_coffee_shop(db=db, coffee_shop_id=coffee_shop_id)

    created_branch = models.Branch(
        name=request.name, location=request.location, coffee_shop_id=coffee_shop_id
    )
    db.add(created_branch)
    db.commit()
    db.refresh(created_branch)
    return created_branch


def is_branch_have_users(branch_id: int, db: Session) -> bool:
    """
    This helper function will be used to check if a branch has users
    *Args:
        branch_id (int): branch id
        db (Session): database session
    *Returns:
        True if the branch has users, False otherwise
    """
    query = db.query(models.User).filter(
        models.User.branch_id == branch_id, models.User.deleted == False
    )
    return query.first() is not None


def find_branch(
    branch_id: int, db: Session, coffee_shop_id: int = None
) -> models.Branch:
    """
    This helper will be used to find a branch by id and coffee shop id
    *Args:
        branch_id (int): branch id to be found
        db (Session): database session
        coffee_shop_id (int): coffee shop id that the branch belongs to
    *Returns:
        the found branch
    """
    query = db.query(models.Branch).filter(
        models.Branch.id == branch_id, models.Branch.deleted == False
    )

    if coffee_shop_id:
        query = query.filter(models.Branch.coffee_shop_id == coffee_shop_id)

    found_branch = query.first()
    if not found_branch:
        raise ShopsAppException(
            message=f"Branch with id={branch_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return found_branch


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
    found_branch = find_branch(
        db=db, branch_id=branch_id, coffee_shop_id=coffee_shop_id
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


def delete_branch(db: Session, branch_id: int, coffee_shop_id: int) -> None:
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
    found_branch = find_branch(
        db=db, branch_id=branch_id, coffee_shop_id=coffee_shop_id
    )

    # check if the branch has users
    if is_branch_have_users(branch_id=branch_id, db=db):
        raise ShopsAppException(
            message="Branch has associated users, please remove them first",
            status_code=status.HTTP_409_CONFLICT,  # conflict error
        )
    found_branch.deleted = True
    db.commit()


def find_all_branches(db: Session, coffee_shop_id: int) -> list[models.Branch]:
    """
    This helper function will be used to get all branches in a coffee shop
    *Args:
        db (Session): database session
        coffee_shop_id (int): coffee shop id
    *Returns:
        a dictionary of all branches in the coffee shop
    """
    query = db.query(models.Branch).filter(
        models.Branch.coffee_shop_id == coffee_shop_id, models.Branch.deleted == False
    )
    return query.all()
