from fastapi import APIRouter, Depends, HTTPException, status, Query
from src import schemas
from sqlalchemy.orm import Session
from src.settings.database import get_db
from src.security.oauth2 import require_role
from src.models.user import UserRole
from src.exceptions.exception import ShopsAppException
from src.utils.control_access import check_if_user_can_access_shop
from src.helpers import report

router = APIRouter(tags=["Reports"], prefix="/reports")


@router.get(
    "/coffee-shops/{coffee_shop_id}/customers-orders",
    response_model=list[schemas.CustomerOrderReport],
)
def list_customers_orders_endpoint(
    coffee_shop_id: int,
    order_by: str = Query("total_paid", regex="^(total_paid|total_orders)$"),
    sort: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([UserRole.ADMIN])),
):
    """
    GET endpoint to list all customers along with their number of orders and total paid
    """
    try:
        check_if_user_can_access_shop(
            user_coffee_shop_id=current_user.coffee_shop_id,
            target_coffee_shop_id=coffee_shop_id,
        )
        return report.list_customers_orders(
            db=db, coffee_shop_id=coffee_shop_id, order_by=order_by, sort=sort
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
