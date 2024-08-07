from pydantic import BaseModel


class BranchUserBase(BaseModel):
    branch_id: int
    manager_id: int
