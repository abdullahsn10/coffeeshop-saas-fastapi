from datetime import datetime, timezone, timedelta
import jwt
from shops_app import schemas
from shops_app.models.user import UserRole
from shops_app.settings.settings import JWT_TOKEN_SETTINGS


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a jwt token with the specified data and expiration time
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
    encoded_jwt = jwt.encode(to_encode,
                             JWT_TOKEN_SETTINGS["PRIVATE_KEY"],
                             algorithm=JWT_TOKEN_SETTINGS["ALGORITHM"])
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
        "coffee_shop_id": coffee_shop_id
    }
    return create_access_token(user_data)


def verify_token(token: str, credentials_exception) -> schemas.TokenData:
    """
    Verify the token and return the token data if the token is valid
    :param token: token to be verified
    :param credentials_exception: exception to be raised if the token is invalid
    :return: token data if the token is valid
    """
    try:
        payload = jwt.decode(token, JWT_TOKEN_SETTINGS["PUBLIC_KEY"],
                             algorithms=JWT_TOKEN_SETTINGS["ALGORITHM"])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        id: int = payload.get("id")
        coffee_shop_id: int = payload.get("coffee_shop_id")
        branch_id: int = payload.get("branch_id")

        # check fields are not None
        if any(field is None for field in (email, role, id, coffee_shop_id, branch_id)):
            raise credentials_exception
        try:
            role_enum = UserRole(role)  # Convert role string back to UserRole enum
        except ValueError:
            raise credentials_exception
        token_data = schemas.TokenData(email=email, role=role_enum,
                                       id=id, coffee_shop_id=coffee_shop_id,
                                       branch_id=branch_id)
        return token_data
    except jwt.InvalidTokenError:
        raise credentials_exception
