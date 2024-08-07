from src import schemas, models
from sqlalchemy.orm import Session
from src.exceptions.exception import *
from src.helpers import coffee_shop


def create(
        request: schemas.BranchBase, coffee_shop_id: int, db: Session,
        user_coffee_shop_id: int
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
        raise ShopsAppException(f'Coffe Shop with id = {coffee_shop_id} does not exist')

    # check if user authorized to create branch in this shop
    if coffee_shop_id != user_coffee_shop_id:
        raise ShopsAppUnAuthorizedException('You are not authorized to create branch on this sop')

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
