from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from src import schemas, models
from src.models.user import UserRole
from src.helpers import user
from src.settings.database import get_db
from src.security.oauth2 import require_role
from src.exceptions.exception import *
from src.utils.control_access import check_if_user_belongs_to_this_coffee_shop

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", response_model=schemas.UserCredentialsInResponse)
def create_user_endpoint(
    request: schemas.UserPOSTRequestBody,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([UserRole.ADMIN])),
):
    """
    POST endpoint to create a user
    """
    try:
        response.status_code = status.HTTP_201_CREATED
        return user.validate_and_create_or_update(
            request=request,
            db=db,
            admin_coffee_shop_id=current_user.coffee_shop_id,
            creation=True,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except ShopsAppUnAuthorizedException as ua:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ua))
    except ShopsAppAlreadyExistsException as ae:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ae))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{user_id}")
def full_update_user_endpoint(
    user_id: int,
    request: schemas.UserPUTRequestBody,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([UserRole.ADMIN])),
):
    try:
        check_if_user_belongs_to_this_coffee_shop(
            user_id=user_id, db=db, coffee_shop_id=current_user.coffee_shop_id
        )
        return user.validate_and_create_or_update(
            request=request,
            db=db,
            admin_coffee_shop_id=current_user.coffee_shop_id,
            creation=False,
            user_id=user_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except ShopsAppUnAuthorizedException as ua:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ua))
    except ShopsAppAlreadyExistsException as ae:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ae))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
