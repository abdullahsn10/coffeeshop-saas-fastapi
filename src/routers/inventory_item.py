from fastapi import APIRouter, Response, Depends, status, HTTPException
from src import schemas, models
from src.settings.database import get_db
from src.security.oauth2 import require_role
from src.helpers import inventory_item, coffee_shop
from src.exceptions.exception import *
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Inventory Items"],
    prefix="/inventory-items",
)


@router.post("/", response_model=schemas.InventoryItemResponse)
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


@router.get("/", response_model=list[schemas.InventoryItemResponse])
def get_all_inventory_items_endpoint(
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    GET endpoint to get all inventory items in the shop
    """
    try:
        return inventory_item.find_all_inventory_items(
            db=db, coffee_shop_id=current_user.coffee_shop_id
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{inventory_item_id}", response_model=schemas.InventoryItemResponse)
def update_inventory_item_endpoint(
    request: schemas.InventoryItemPUTRequestBody,
    inventory_item_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    PUT endpoint to update an inventory item in the shop
    """
    try:
        return inventory_item.update_inventory_item(
            request=request,
            db=db,
            inventory_item_id=inventory_item_id,
            admin_coffee_shop_id=current_user.coffee_shop_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{inventory_item_id}")
def delete_inventory_item_endpoint(
    inventory_item_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
    DELETE endpoint to delete an inventory item in the shop
    """
    try:
        response.status_code = status.HTTP_204_NO_CONTENT
        inventory_item.delete_inventory_item(
            inventory_item_id=inventory_item_id,
            db=db,
            admin_coffee_shop_id=current_user.coffee_shop_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
