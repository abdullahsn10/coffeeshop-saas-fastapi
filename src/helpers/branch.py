from typing import Dict

from src import schemas, models
from sqlalchemy.orm import Session
from src.exceptions.exception import *
from src.helpers import coffee_shop


def create(
        request: schemas.BranchBase,
        coffee_shop_id: int,
        db: Session,
        user_coffee_shop_id: int,
) -> models.Branch:
    """
    This helper function will be used to create a new branch
    *Args:
        request (schemas.BranchBase): schema instance that contains branch details
        db (Session): database session
    *Returns:
        the created branch
    """
    # check if the shop exists
    if not coffee_shop.find_by_id(db=db, id=coffee_shop_id):
        raise ShopsAppException(f"Coffe Shop with id = {coffee_shop_id} does not exist")

    # check if user authorized to create branch in this shop
    if coffee_shop_id != user_coffee_shop_id:
        raise ShopsAppUnAuthorizedException(
            "You are not authorized to create branch on this shop"
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


def find_by_id(db: Session, id: int) -> models.Branch:
    """
    This helper function will be used to find a branch by id
    :param db: db session
    :param id: the id of the branch needed to be found
    :return: the found branch instance
    """
    return db.query(models.Branch).filter(models.Branch.id == id).first()


def update(request: schemas.BranchBase, db: Session, id: int,
           coffee_shop_id: int,
           user_coffee_shop_id: int) -> models.Branch:
    """
    This helper function will be used to update a branch
    :param request: the branch information
    :param db: db session
    :param id: the id of the branch needed to be updated
    :param coffee_shop_id: the coffee shop id of the branch
    :param user_coffee_shop_id: the user coffee shop id
    :return: updated branch instance
    """

    # check coffee_shop exists, branch exits
    if not coffee_shop.find_by_id(db=db, id=coffee_shop_id):
        raise ShopsAppException(f'Coffee Shop with id = {coffee_shop_id} does not exist')

    found_branch = find_by_id(db=db, id=id)
    if not found_branch:
        raise ShopsAppException(f'Branch with id = {id} does not exist')

    # check if the user authorized to update on this coffee shop
    if user_coffee_shop_id != coffee_shop_id:
        raise ShopsAppUnAuthorizedException(f'You are not authorized to update branch on this shop')

    # check if the branch belongs to this coffee shop
    if get_coffee_shop_id(db=db, branch_id=found_branch.id) != coffee_shop_id:
        raise ShopsAppException(f'Branch with id = {id} does not exist in this coffee shop')

    # Update all fields of the branch object based on the request
    update_data = request.model_dump(
        exclude_unset=True
    )  # Get dictionary of all set fields in request
    for field, value in update_data.items():
        setattr(found_branch, field, value)
    db.commit()
    db.refresh(found_branch)
    return found_branch


def delete(db: Session, id: int,
           coffee_shop_id: int,
           user_coffee_shop_id: int) -> dict[str, str]:
    """
    This helper function will be used to delete a branch
    :param db: db session
    :param id: the id of the branch needed to be deleted
    :param coffee_shop_id: the coffee shop id of the branch
    :param user_coffee_shop_id: the user coffee shop id
    :return: str representation of the deleted branch
    """

    # check coffee_shop exists, branch exits
    if not coffee_shop.find_by_id(db=db, id=coffee_shop_id):
        raise ShopsAppException(f'Coffee Shop with id = {coffee_shop_id} does not exist')

    found_branch = find_by_id(db=db, id=id)
    if not found_branch:
        raise ShopsAppException(f'Branch with id = {id} does not exist')

    # check if the user authorized to delete on this coffee shop
    if user_coffee_shop_id != coffee_shop_id:
        raise ShopsAppUnAuthorizedException(f'You are not authorized to update branch on this shop')

    # check if the branch belongs to this coffee shop
    if get_coffee_shop_id(db=db, branch_id=found_branch.id) != coffee_shop_id:
        raise ShopsAppException(f'Branch with id = {id} does not exist in this coffee shop')

    db.delete(found_branch)
    db.commit()
    return {'detail': 'Branch deleted successfully'}