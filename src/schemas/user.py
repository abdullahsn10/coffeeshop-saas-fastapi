from pydantic import BaseModel
from src.models.user import UserRole


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


class UserPOSTRequestBody(UserBase):
    """
    Pydantic schema for User POST request body
    """

    role: UserRole
    branch_id: int

    class Config:
        orm_mode = True


class UserPUTRequestBody(UserPOSTRequestBody):
    """
    Pydantic schema for User PUT request body
    """

    class Config:
        orm_mode = True


class UserPATCHRequestBody(BaseModel):
    """
    Pydantic schema for User PATCH request body
    """

    first_name: str = None
    last_name: str = None
    email: str = None
    phone_no: str = None
    password: str = None

    class Config:
        orm_mode = True
