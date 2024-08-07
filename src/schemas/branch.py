from pydantic import BaseModel


class BranchBase(BaseModel):
    name: str
    location: str


class BranchResponseBody(BranchBase):
    id: int
    coffee_shop_id: int

    class Config:
        orm_mode = True
