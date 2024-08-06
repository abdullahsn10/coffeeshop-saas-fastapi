from shops_app import schemas, models
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
