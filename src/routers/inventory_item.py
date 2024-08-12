from fastapi import APIRouter, Response, Depends, status, HTTPException
from src import schemas, models
from src.settings.database import get_db
from src.security.oauth2 import require_role
from src.helpers import inventory_item, coffee_shop
from src.exceptions.exception import *
from sqlalchemy.orm import Session
from src.utils.control_access import check_if_user_can_access_this_item

router = APIRouter(
    tags=["Inventory Items"],
    prefix="/inventory-items",
)


@router.post("/", response_model=schemas.InventoryItemGETResponse)
def create_inventory_item_endpoint(
    request: schemas.InventoryItemPOSTRequestBody,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    POST endpoint to create an inventory item in the shop
    """
    try:
        response.status_code = status.HTTP_201_CREATED
        created_inventory_item = inventory_item.create_inventory_item(
            request=request, coffee_shop_id=current_user.coffee_shop_id, db=db
        )
        return created_inventory_item
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=list[schemas.InventoryItemGETResponse])
def get_all_inventory_items_endpoint(
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    try:
        return coffee_shop.get_all_inventory_items_in_the_shop(
            db=db, coffee_shop_id=current_user.coffee_shop_id
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{inventory_item_id}")
def update_inventory_item_endpoint(
    request: schemas.InventoryItemPUTRequestBody,
    inventory_item_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    try:
        check_if_user_can_access_this_item(
            item_id=inventory_item_id,
            db=db,
            admin_coffee_shop_id=current_user.coffee_shop_id,
            is_inventory_item=True,
        )
        return inventory_item.update_inventory_item(
            request=request, db=db, inventory_item_id=inventory_item_id
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
