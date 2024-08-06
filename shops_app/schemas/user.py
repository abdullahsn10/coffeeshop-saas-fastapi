from pydantic import BaseModel
from shops_app.models.user import UserRole


class UserBase(BaseModel):
    """
    Pydantic schema for User
    """
    first_name: str
    last_name: str
    email: str
    phone_no: str
    password: str

    class Config:
        orm_mode = True


class UserFullInformation(UserBase):
    """
    Pydantic schema for User with full information
    """
    id: int
    role: UserRole
    branch_id: int

    class Config:
        orm_mode = True


class UserCredentialsInResponse(BaseModel):
    """
    Pydantic schema for User with email and phone_no
    """
    email: str
    phone_no: str

    class Config:
        orm_mode = True
