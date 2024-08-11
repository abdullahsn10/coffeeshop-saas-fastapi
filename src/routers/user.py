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
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{user_id}", response_model=schemas.UserCredentialsInResponse)
def full_update_user_endpoint(
    user_id: int,
    request: schemas.UserPUTRequestBody,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([UserRole.ADMIN])),
):
    """
    PUT endpoint to fully update a user
    """
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
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch("/{user_id}", response_model=schemas.UserCredentialsInResponse)
def partial_update_user_endpoint(
    user_id: int,
    request: schemas.UserPATCHRequestBody,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([UserRole.ADMIN])),
):
    """
    PATCH endpoint to partially update a user
    """
    try:
        check_if_user_belongs_to_this_coffee_shop(
            user_id=user_id, db=db, coffee_shop_id=current_user.coffee_shop_id
        )
        return user.validate_and_partial_update(
            request=request,
            db=db,
            user_id=user_id,
            admin_coffee_shop_id=current_user.coffee_shop_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=list[schemas.UserGETResponse])
def get_all_users_endpoint(
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([UserRole.ADMIN])),
):
    """
    GET endpoint to get all users
    """
    try:
        return user.find_all_users_in_this_shop(
            db=db, coffee_shop_id=current_user.coffee_shop_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{user_id}", response_model=schemas.UserGETResponse)
def get_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([UserRole.ADMIN])),
):
    """
    GET endpoint to get a user
    """
    try:
        check_if_user_belongs_to_this_coffee_shop(
            user_id=user_id, db=db, coffee_shop_id=current_user.coffee_shop_id
        )
        return user.find_user_by_id(db=db, user_id=user_id)
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{user_id}")
def delete_user_endpoint(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([UserRole.ADMIN])),
):
    """
    DELETE endpoint to delete a user
    """
    try:
        check_if_user_belongs_to_this_coffee_shop(
            user_id=user_id, db=db, coffee_shop_id=current_user.coffee_shop_id
        )
        response.status_code = status.HTTP_204_NO_CONTENT
        user.delete_user_by_id(db=db, user_id=user_id)
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
