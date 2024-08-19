from pydantic import BaseModel


class BranchBase(BaseModel):
    """
    Pydantic model for Branch
    """

    name: str
    location: str


class BranchResponse(BranchBase):
    """
    Pydantic model for Branch in ResponseBody, with id and coffee_shop_id
    """

    id: int
    coffee_shop_id: int

    class Config:
        orm_mode = True
