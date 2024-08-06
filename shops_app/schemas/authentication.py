from pydantic import BaseModel
from shops_app.schemas.coffee_shop import CoffeeShopBase
from shops_app.schemas.user import UserBase


class SignUpIn(BaseModel):
    """
    pydantic schema that will be used as request body in the
    signup endpoint, it contains shop details and admin details
    """
    shop_details: CoffeeShopBase
    admin_details: UserBase


class LoginIn(BaseModel):
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
