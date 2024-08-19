from fastapi import APIRouter, Depends, Response, HTTPException, status
from src import schemas
from sqlalchemy.orm import Session
from src.settings.database import get_db
from src.security.oauth2 import require_role
from src.models.user import UserRole
from src.helpers import customer
from src.exceptions.exception import ShopsAppException

router = APIRouter(
    tags=["Customers"],
    prefix="/customer",
)


@router.put("/{customer_id}", response_model=schemas.CustomerResponse)
def update_customer_endpoint(
    customer_id: int,
    request: schemas.CustomerPUTRequestBody,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(
        require_role([UserRole.ADMIN, UserRole.CASHIER])
    ),
):
    """
    PUT endpoint to fully update a customer
    """
    try:
        return customer.update_customer(
            request=request,
            db=db,
            coffee_shop_id=current_user.coffee_shop_id,
            customer_id=customer_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
