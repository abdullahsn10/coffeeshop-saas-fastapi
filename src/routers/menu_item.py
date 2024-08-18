from fastapi import APIRouter, Response, Depends, status, HTTPException
from src import schemas, models
from src.models.user import UserRole
from src.settings.database import get_db
from src.security.oauth2 import require_role
from src.helpers import menu_item, coffee_shop
from src.exceptions.exception import *
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Menu Items"],
    prefix="/menu-items",
)


@router.post("/", response_model=schemas.MenuItemGETResponse)
def create_menu_item_endpoint(
    request: schemas.MenuItemPOSTRequestBody,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([UserRole.ADMIN])),
):
    """
    POST endpoint to create a menu item in the shop
    """
    try:
        response.status_code = status.HTTP_201_CREATED
        created_inventory_item = menu_item.create_menu_item(
            request=request, coffee_shop_id=current_user.coffee_shop_id, db=db
        )
        return created_inventory_item
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=list[schemas.MenuItemGETResponse])
def get_all_menu_items_endpoint(
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(
        require_role(
            [UserRole.ADMIN, UserRole.ORDER_RECEIVER, UserRole.CASHIER, UserRole.CHEF]
        )
    ),
):
    """
    GET endpoint to get all menu items in the shop
    """
    try:
        return menu_item.find_all_menu_items(
            db=db, coffee_shop_id=current_user.coffee_shop_id
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{menu_item_id}", response_model=schemas.MenuItemGETResponse)
def update_menu_item_endpoint(
    request: schemas.MenuItemPUTRequestBody,
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    PUT endpoint to update a specific menu item
    """
    try:
        return menu_item.update_menu_item(
            request=request,
            db=db,
            menu_item_id=menu_item_id,
            admin_coffee_shop_id=current_user.coffee_shop_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{menu_item_id}")
def delete_menu_item_endpoint(
    menu_item_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    DELETE endpoint to delete a specific menu item in the shop
    """
    try:
        response.status_code = status.HTTP_204_NO_CONTENT
        menu_item.delete_menu_item(
            menu_item_id=menu_item_id,
            db=db,
            admin_coffee_shop_id=current_user.coffee_shop_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
