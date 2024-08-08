from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from src.security.jwt import verify_token
from src.models.user import UserRole
from src import schemas
from src.helpers import user
from sqlalchemy.orm import Session
from src.settings.database import get_db

# define the route from where the fastapi will fetch the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> schemas.TokenData:
    """
    This function will return the current user based on the token data after
    verifying his/her token
    *Args:
        token: the token obtained as a dependency from oauth2_schem
    *Returns:
        Token Data contains the user's data extracted from the token if it
        is valid
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
    *Args:
        allowed_roles: a list of allowed roles that the current user must have to access
    *Returns:
        The user data extracted from the token if the user has the proper role,
        raise exception otherwise.
    """

    def role_checker(current_user: schemas.TokenData = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the necessary permissions",
            )
        return current_user

    return role_checker
