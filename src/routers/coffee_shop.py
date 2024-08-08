from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from src import schemas, models
from src.security.oauth2 import require_role
from src.settings.database import get_db
from src.helpers import coffee_shop, branch, branch_user
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
        return coffee_shop.update(request=request, db=db, id=coffee_shop_id)
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except ShopsAppUnAuthorizedException as ua:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ua))
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
        created_branch = branch.create(
            request=request, coffee_shop_id=coffee_shop_id, db=db
        )
        branch_user_relationship = branch_user.create(
            manager_id=current_user.id, branch_id=created_branch.id, db=db
        )
        return created_branch
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except ShopsAppUnAuthorizedException as ua:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ua))
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
        return branch.update(
            request=request, db=db, id=branch_id, coffee_shop_id=coffee_shop_id
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except ShopsAppUnAuthorizedException as ua:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ua))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{coffee_shop_id}/branches/{branch_id}", response_model=dict[str, str])
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
        check_if_user_can_access_shop(
            user_coffee_shop_id=current_user.coffee_shop_id,
            target_coffee_shop_id=coffee_shop_id,
        )
        return branch.delete(db=db, id=branch_id, coffee_shop_id=coffee_shop_id)
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except ShopsAppUnAuthorizedException as ua:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ua))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
