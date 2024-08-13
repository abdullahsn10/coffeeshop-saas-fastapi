from fastapi import APIRouter, HTTPException, Depends, Response, status
from src import schemas
from src.models.user import UserRole
from sqlalchemy.orm import Session
from src.settings.database import get_db
from src.exceptions.exception import ShopsAppException
from src.security.oauth2 import require_role
from src.helpers import order

router = APIRouter(
    tags=["Orders"],
    prefix="/orders",
)


@router.post("", response_model=schemas.OrderPOSTResponseBody)
def place_an_order_endpoint(
    request: schemas.OrderPOSTRequestBody,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(
        require_role([UserRole.ORDER_RECEIVER, UserRole.CASHIER])
    ),
):
    try:
        return order.place_an_order(
            request=request,
            coffee_shop_id=current_user.coffee_shop_id,
            issuer_id=current_user.id,
            db=db,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
