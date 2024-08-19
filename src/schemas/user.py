from pydantic import BaseModel, root_validator
from src.models.user import UserRole
from typing import Optional
from src.exceptions.exception import ShopsAppException


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

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_no: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    branch_id: Optional[int] = None

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    """
    Pydantic schema for User GET response
    """

    id: int
    first_name: str
    last_name: str
    email: str
    phone_no: str
    role: UserRole
    branch_id: int

    class Config:
        orm_mode = True


class UserInRestorePATCHRequestBody(BaseModel):
    """
    Pydantic schema for User PATCH request body to restore a deleted user
    """

    email: Optional[str] = None
    phone_no: Optional[str] = None
    branch_id: int
