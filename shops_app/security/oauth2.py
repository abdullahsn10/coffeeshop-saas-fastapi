from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from shops_app.security.jwt import verify_token
from shops_app.models.user import UserRole
from shops_app import schemas
from shops_app.helpers import user
from sqlalchemy.orm import Session
from shops_app.settings.database import get_db

# define the route from where the fastapi will fetch the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> schemas.TokenData:
    """
    This function will return the current user based on the token data
    :param token: token to verify
    :param db: sqlalchemy session
    :return: the current user data from the token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    return token_data


def require_role(allowed_roles: list[UserRole]):
    """
    This function will check if the current user has the necessary role to access the route
    :param allowed_roles: list of roles that are allowed to access the route
    :return: the current user data if the role is allowed, else raise an exception
    """
    def role_checker(current_user: schemas.TokenData = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the necessary permissions"
            )
        return current_user

    return role_checker

