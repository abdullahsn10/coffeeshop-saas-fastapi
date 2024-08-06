from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from shops_app import schemas, models
from shops_app.security.oauth2 import require_role
from shops_app.settings.database import get_db

router = APIRouter(
    tags=["Coffee Shops"],
    prefix="/coffee-shops",
)


@router.put('/{coffee_shop_id}')
def update_coffee_shop(coffee_shop_id: int,
                       request: schemas.CoffeeShopBase,
                       db: Session = Depends(get_db),
                       current_user: schemas.TokenData = Depends(require_role(
                           [models.UserRole.ADMIN]
                       ))):
    return 'Hello world'
