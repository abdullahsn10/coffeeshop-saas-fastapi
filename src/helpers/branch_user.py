from src import schemas, models
from sqlalchemy.orm import Session


def create(request: schemas.BranchUserBase, db: Session) -> models.BranchUser:
    """
    This helper function will be used to create a relationship between branch and user(Admin)
    """
    created_relationship_instance = models.BranchUser(
        **request.model_dump(exclude_unset=True)
    )
    db.add(created_relationship_instance)
    db.commit()
    db.refresh(created_relationship_instance)
    return created_relationship_instance
