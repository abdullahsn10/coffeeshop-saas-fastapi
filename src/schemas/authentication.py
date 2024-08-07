from pydantic import BaseModel
from src.schemas.branch import BranchBase
from src.schemas.coffee_shop import CoffeeShopBase
from src.schemas.user import UserBase
from src.models.user import UserRole


class SignUpRequestBody(BaseModel):
    """
    pydantic schema that will be used as request body in the
    signup endpoint, it contains shop details and admin details
    """

    shop_details: CoffeeShopBase
    branch_details: BranchBase
    admin_details: UserBase


class LoginRequestBody(BaseModel):
    """
    pydantic schema that will be used as request body in the
    login endpoint, it contains user credentials
    """

    username: str
    password: str


class Token(BaseModel):
    """
    pydantic schema for JWT Token, used in returning a token to the user
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    pydantic schema for the token data
    """

    id: int
    email: str
    role: UserRole
    branch_id: int
    coffee_shop_id: int
