from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src import schemas, models
from src.security.oauth2 import require_role
from src.settings.database import get_db
from src.helpers import coffee_shop, branch
from src.exceptions.exception import *

router = APIRouter(
    tags=["Coffee Shops"],
    prefix="/coffee-shops",
)


@router.put("/{coffee_shop_id}")
def update_coffee_shop_endpoint(
    coffee_shop_id: int,
    request: schemas.CoffeeShopBase,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    PUT endpoint to fully update a specific coffee shop
    """
    try:
        return coffee_shop.update(
            request=request,
            db=db,
            id=coffee_shop_id,
            user_coffe_shop_id=current_user.coffee_shop_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except ShopsAppUnAuthorizedException as ua:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ua))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/{coffee_shop_id}/branches")
def create_branch_endpoint(
    coffee_shop_id: int,
    request: schemas.BranchBase,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    POST endpoint to create a branch for a specific coffee shop
    """
    try:
        return branch.create(
            request=request,
            coffee_shop_id=coffee_shop_id,
            db=db,
            user_coffee_shop_id=current_user.coffee_shop_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except ShopsAppUnAuthorizedException as ua:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ua))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{coffee_shop_id}/branches/{branch_id}")
def update_branch_endpoint(
    coffee_shop_id: int,
    branch_id: int,
    request: schemas.BranchBase,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    PUT endpoint to update a specific branch for a specific coffee shop
    """

    try:
        return branch.update(
            request=request,
            db=db,
            id=branch_id,
            coffee_shop_id=coffee_shop_id,
            user_coffee_shop_id=current_user.coffee_shop_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except ShopsAppUnAuthorizedException as ua:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ua))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{coffee_shop_id}/branches/{branch_id}")
def delete_branch_endpoint(
    coffee_shop_id: int,
    branch_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    DELETE endpoint to delete a branch for a specific coffee shop
    """

    try:
        return branch.delete(
            db=db,
            id=branch_id,
            coffee_shop_id=coffee_shop_id,
            user_coffee_shop_id=current_user.coffee_shop_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except ShopsAppUnAuthorizedException as ua:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ua))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
