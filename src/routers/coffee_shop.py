from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from src import schemas, models
from src.security.oauth2 import require_role
from src.settings.database import get_db
from src.helpers import coffee_shop, branch
from src.exceptions.exception import *
from src.utils.control_access import check_if_user_can_access_shop

router = APIRouter(
    tags=["Coffee Shops"],
    prefix="/coffee-shops",
)


@router.put("/{coffee_shop_id}", response_model=schemas.CoffeeShopBase)
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
        check_if_user_can_access_shop(
            user_coffee_shop_id=current_user.coffee_shop_id,
            target_coffee_shop_id=coffee_shop_id,
        )
        return coffee_shop.update_coffee_shop(
            request=request, db=db, coffee_shop_id=coffee_shop_id
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/{coffee_shop_id}/branches", response_model=schemas.BranchResponseBody)
def create_branch_endpoint(
    coffee_shop_id: int,
    request: schemas.BranchBase,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    POST endpoint to create a branch for a specific coffee shop
    """
    try:
        check_if_user_can_access_shop(
            user_coffee_shop_id=current_user.coffee_shop_id,
            target_coffee_shop_id=coffee_shop_id,
        )
        response.status_code = status.HTTP_201_CREATED
        created_branch = branch.create_branch(
            request=request, coffee_shop_id=coffee_shop_id, db=db
        )
        return created_branch
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put(
    "/{coffee_shop_id}/branches/{branch_id}", response_model=schemas.BranchResponseBody
)
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
        check_if_user_can_access_shop(
            user_coffee_shop_id=current_user.coffee_shop_id,
            target_coffee_shop_id=coffee_shop_id,
        )
        return branch.update_branch(
            request=request, db=db, branch_id=branch_id, coffee_shop_id=coffee_shop_id
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{coffee_shop_id}/branches/{branch_id}", response_model=dict[str, str])
def delete_branch_endpoint(
    coffee_shop_id: int,
    branch_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    DELETE endpoint to delete a branch for a specific coffee shop
    """

    try:
        check_if_user_can_access_shop(
            user_coffee_shop_id=current_user.coffee_shop_id,
            target_coffee_shop_id=coffee_shop_id,
        )
        response.status_code = status.HTTP_204_NO_CONTENT
        branch.delete_branch_by_id(
            db=db, branch_id=branch_id, coffee_shop_id=coffee_shop_id
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
