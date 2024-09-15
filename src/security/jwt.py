from datetime import datetime, timezone, timedelta
import jwt
from src import schemas
from src.models.user import UserRole
from src.settings.settings import JWT_TOKEN_SETTINGS
from typing import Optional


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a jwt token with the specified data and expiration time
    *Args:
        data: data to be encoded in the token
        expires_delta: expiration time for the token
    *Returns:
        jwt token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    # Convert the role to its string representation if it exists
    if "role" in to_encode and isinstance(to_encode["role"], UserRole):
        to_encode["role"] = to_encode["role"].value

    # create jwt token with the specified data
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_TOKEN_SETTINGS["PRIVATE_KEY"],
        algorithm=JWT_TOKEN_SETTINGS["ALGORITHM"],
    )
    return encoded_jwt


def generate_token_for_user(user: schemas.UserFullInformation, coffee_shop_id: int):
    """
    Call this function to generate a jwt token for the user
    *Args:
        User object for which the token is to be generated
    """
    user_data = {
        "id": user.id,
        "sub": user.email,
        "role": user.role,
        "branch_id": user.branch_id,
        "coffee_shop_id": coffee_shop_id,
    }
    return create_access_token(user_data)


def verify_token(token: str, credentials_exception) -> schemas.TokenData:
    """
    Verify the token and return the token data if the token is valid
    *Args:
        token: token to be verified
        credentials_exception: exception to be raised if the token is invalid
    *Returns:
        token data if the token is valid
    """
    try:
        payload = jwt.decode(
            token,
            JWT_TOKEN_SETTINGS["PUBLIC_KEY"],
            algorithms=JWT_TOKEN_SETTINGS["ALGORITHM"],
        )

        required_fields = ["sub", "role", "id", "coffee_shop_id", "branch_id"]

        if not all(field in payload for field in required_fields):
            raise credentials_exception

        try:
            role_enum = UserRole(
                payload["role"]
            )  # Convert role string back to UserRole enum
        except ValueError:
            raise credentials_exception

        token_data = schemas.TokenData(
            email=payload["sub"],
            role=role_enum,
            id=payload["id"],
            coffee_shop_id=payload["coffee_shop_id"],
            branch_id=payload["branch_id"],
        )
        return token_data
    except jwt.InvalidTokenError:
        raise credentials_exception
