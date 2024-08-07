from typing import Dict

from src import schemas, models
from sqlalchemy.orm import Session
from src.exceptions.exception import *
from src.helpers import coffee_shop


def create(
    request: schemas.BranchBase, coffee_shop_id: int, db: Session
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
    *Args:
        db (Session): database session
        id (int): branch id

    *Returns:
        the found branch
    """
    return (
        db.query(models.Branch)
        .filter(models.Branch.id == id, models.Branch.deleted == False)
        .first()
    )


def find_by_id_and_shop_id(id: int, db: Session, coffee_shop_id: int) -> models.Branch:
    """
    This helper will be used to find a branch by id and coffee shop id
    in otherwords, it will check if the branch belongs to the shop
    *Args:
        id (int): branch id to be found
        db (Session): database session
        coffee_shop_id (int): coffee shop id that the branch belongs to
    *Returns:
        the found branch
    """

    return (
        db.query(models.Branch)
        .filter(
            models.Branch.id == id,
            models.Branch.deleted == False,
            models.Branch.coffee_shop_id == coffee_shop_id,
        )
        .first()
    )


def update(
    request: schemas.BranchBase, db: Session, id: int, coffee_shop_id: int
) -> models.Branch:
    """
    This helper function will be used to update a branch
    *Args:
        request (schemas.BranchBase): schema instance that contains branch details
        db (Session): database session
        id (int): branch id
        coffee_shop_id (int): coffee shop id
        user_coffee_shop_id (int): user coffee shop id
    *Returns:
        the updated branch
    """

    # # check coffee_shop exists, branch exits
    # if not coffee_shop.find_by_id(db=db, id=coffee_shop_id):
    #     raise ShopsAppException(
    #         f"Coffee Shop with id = {coffee_shop_id} does not exist"
    #     )
    #
    # found_branch = find_by_id(db=db, id=id)
    # if not found_branch:
    #     raise ShopsAppException(f"Branch with id = {id} does not exist")
    #
    # if get_coffee_shop_id(db=db, branch_id=found_branch.id) != coffee_shop_id:
    #     raise ShopsAppException(
    #         f"Branch with id = {id} does not exist in this coffee shop"
    #     )

    # check if the branch belongs to this coffee shop
    found_branch = find_by_id_and_shop_id(db=db, id=id, coffee_shop_id=coffee_shop_id)
    if not found_branch:
        raise ShopsAppException(
            f"Branch with id = {id} does not exist in this coffee shop"
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


def delete(db: Session, id: int, coffee_shop_id: int) -> dict[str, str]:
    """
    This helper function will be used to delete a branch
    *Args:
        db (Session): database session
        id (int): branch id
        coffee_shop_id (int): coffee shop id
        user_coffee_shop_id (int): user coffee shop id
    *Returns:
        a dict representation of the deleted branch
    """

    # # check coffee_shop exists, branch exits
    # if not coffee_shop.find_by_id(db=db, id=coffee_shop_id):
    #     raise ShopsAppException(
    #         f"Coffee Shop with id = {coffee_shop_id} does not exist"
    #     )
    #
    # found_branch = find_by_id(db=db, id=id)
    # if not found_branch:
    #     raise ShopsAppException(f"Branch with id = {id} does not exist")
    #
    # if get_coffee_shop_id(db=db, branch_id=found_branch.id) != coffee_shop_id:
    #     raise ShopsAppException(
    #         f"Branch with id = {id} does not exist in this coffee shop"
    #     )

    # check if the branch belongs to this coffee shop
    found_branch = find_by_id_and_shop_id(db=db, id=id, coffee_shop_id=coffee_shop_id)
    if not found_branch:
        raise ShopsAppException(
            f"Branch with id = {id} does not exist in this coffee shop"
        )

    found_branch.deleted = True
    db.commit()
    return {"detail": "Branch deleted successfully"}
