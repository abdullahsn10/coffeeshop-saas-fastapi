from src import schemas, models
from sqlalchemy.orm import Session


def create(request: schemas.BranchBase, coffee_shop_id: int,
           db: Session) -> models.Branch:
    """
    This helper function will be used to create a new branch
    *Args:
        request (schemas.BranchBase): schema instance that contains branch details
        db (Session): database session
    *Returns:
        the created branch
    """
    created_branch = models.Branch(
        name=request.name,
        location=request.location,
        coffee_shop_id=coffee_shop_id
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
