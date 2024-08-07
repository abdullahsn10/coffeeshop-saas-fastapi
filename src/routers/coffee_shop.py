from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src import schemas, models
from src.security.oauth2 import require_role
from src.settings.database import get_db
from src.helpers import coffee_shop
from src.exceptions.exception import *

router = APIRouter(
    tags=["Coffee Shops"],
    prefix="/coffee-shops",
)


@router.put("/{coffee_shop_id}")
def update_coffee_shop(
    coffee_shop_id: int,
    request: schemas.CoffeeShopBase,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([models.UserRole.ADMIN])),
):
    """
        Fully update coffee shop endpointsss
    """
    try:
        return coffee_shop.update(
            request=request, id=coffee_shop_id, db=db, user_id=current_user.id
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except ShopsAppUnAuthorizedException as ua:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ua))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
