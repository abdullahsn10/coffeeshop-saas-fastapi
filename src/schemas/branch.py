from pydantic import BaseModel


class BranchBase(BaseModel):
    name: str
    location: str
