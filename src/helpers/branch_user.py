from src import schemas, models
from sqlalchemy.orm import Session


def create(branch_id: int, manager_id: int, db: Session) -> models.BranchUser:
    """
    This helper function will be used to create a relationship between branch and user(Admin)
    *Args:
        branch_id (int): the branch id
        manager_id (int): the manager's of the branch id
        db (Session): the database session
    *Returns:
        The created branchUser instance
    """
    created_relationship_instance = models.BranchUser(
        branch_id=branch_id, manager_id=manager_id
    )
    db.add(created_relationship_instance)
    db.commit()
    db.refresh(created_relationship_instance)
    return created_relationship_instance
