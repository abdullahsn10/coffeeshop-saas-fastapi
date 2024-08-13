import datetime
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import status
from src import schemas, models
from src.exceptions import ShopsAppException
from src.helpers import customer, menu_item
from src.models.order import OrderStatus


def validate_order_items(
    items_list: list[schemas.MenuItemInPOSTOrderRequestBody],
    coffee_shop_id: int,
    db: Session,
):
    """
    This helper function used to validate all items in an order that they are exist
    *Args:
        items_list (list[schemas.MenuItemInPOSTOrderRequestBody]): a list of order items
        db (Session): a database session
    *Returns:
        raise ShopsAppException in case of violation
    """
    for item in items_list:
        if not menu_item.find_menu_item(
            db=db, menu_item_id=item.id, coffee_shop_id=coffee_shop_id
        ):
            raise ShopsAppException(
                message="Menu item does not exist",
                status_code=status.HTTP_400_BAD_REQUEST,
            )


def create_order(
    customer_id: int,
    issuer_id: int,
    db: Session,
    order_items: list[schemas.MenuItemInPOSTOrderRequestBody],
) -> models.Order:
    """
    This helper function used to create a new order instance
    *Args:
        customer_id (int): the customer id
        issuer_id (int): the issuer id of the order
        db (Session): a database session
    *Returns:
        the created order instance
    """
    created_order = models.Order(
        customer_id=customer_id,
        issuer_id=issuer_id,
        status=OrderStatus.PENDING,
        issue_date=datetime.now(),
    )
    db.add(created_order)
    db.commit()
    db.refresh(created_order)

    # create order details
    for item in order_items:
        db.add(
            models.OrderItem(
                order_id=created_order.id,
                item_id=item.id,
                quantity=item.quantity,
            )
        )
        db.commit()

    return created_order


def place_an_order(
    request: schemas.OrderPOSTRequestBody,
    coffee_shop_id: int,
    issuer_id: int,
    db: Session,
) -> schemas.OrderPOSTResponseBody:
    """
    This helper function used to place an order
    *Args:
        request (schemas.OrderPOSTRequestBody): details of the order
        coffee_shop_id (int): id of the coffee shop to create the order for
        issuer_id (int): id of the user (chef or order_receiver) who created the order
        db (Session): database session
    *Returns:
        the created order details (schemas.OrderPOSTResponseBody)
    """

    customer_details: schemas.CustomerPOSTRequestBody = request.customer_details
    order_items: list[schemas.MenuItemInPOSTOrderRequestBody] = request.order_items

    validate_order_items(items_list=order_items, db=db, coffee_shop_id=coffee_shop_id)

    created_customer_instance = customer.create_customer(
        request=customer_details, db=db, coffee_shop_id=coffee_shop_id
    )

    created_order = create_order(
        customer_id=created_customer_instance.id,
        issuer_id=issuer_id,
        db=db,
        order_items=order_items,
    )

    return schemas.OrderPOSTResponseBody(
        id=created_order.id,
        customer_phone_no=created_customer_instance.phone_no,
        status=created_order.status,
    )
