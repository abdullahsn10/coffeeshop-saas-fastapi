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
    """
    POST endpoint to place an order
    """
    try:
        response.status_code = status.HTTP_201_CREATED
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


@router.get("/", response_model=list[schemas.OrderGETResponse])
def get_all_orders_endpoint(
    order_status: str = "PENDING",
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(
        require_role([UserRole.CHEF, UserRole.CASHIER, UserRole.ADMIN])
    ),
):
    """
    GET endpoint to get all orders
    """
    try:
        return order.get_all_orders_details(
            status=order_status,
            db=db,
            coffee_shop_id=current_user.coffee_shop_id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{order_id}", response_model=schemas.OrderGETResponse)
def get_order_details_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(
        require_role([UserRole.ORDER_RECEIVER, UserRole.CASHIER])
    ),
):
    """
    GET endpoint to get a specific order
    """
    try:
        return order.get_order_details(
            order_id=order_id,
            coffee_shop_id=current_user.coffee_shop_id,
            db=db,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch("/{order_id}/status")
def update_order_status_endpoint(
    request: schemas.OrderStatusPATCHRequestBody,
    order_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(
        require_role([UserRole.CHEF, UserRole.CASHIER])
    ),
):
    """
    PATCH endpoint to update a specific order's status
    """
    try:
        order.update_order_status(
            request=request,
            coffee_shop_id=current_user.coffee_shop_id,
            db=db,
            order_id=order_id,
            user_role=current_user.role,
            user_id=current_user.id,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch("/{order_id}/assign/{user_id}")
def assign_order_endpoints(
    order_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(
        require_role([UserRole.ADMIN, UserRole.CHEF])
    ),
):
    """
    PATCH endpoint to assign a specific order to a specific user (CHEF)
    """
    try:
        order.assign_order(
            order_id=order_id,
            chef_id=user_id,
            coffee_shop_id=current_user.coffee_shop_id,
            db=db,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
