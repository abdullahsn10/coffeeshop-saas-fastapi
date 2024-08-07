from pydantic import BaseModel


class BranchUserBase(BaseModel):
    """
    Pydantic model for BranchUser relationship (manager-branches)
    """

    branch_id: int
    manager_id: int
