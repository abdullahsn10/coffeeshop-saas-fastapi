from fastapi import APIRouter, Response, Depends, status, HTTPException
from src import schemas, models
from src.settings.database import get_db
from src.security.oauth2 import require_role
from src.helpers import inventory_item
from src.exceptions.exception import *
from sqlalchemy.orm import Session

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
