import datetime
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import status
from src import schemas, models
from src.exceptions import ShopsAppException
from src.helpers import customer, menu_item, user, coffee_shop
from src.models.order import OrderStatus
from src.models.user import UserRole


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


def find_order(order_id: int, db: Session, coffee_shop_id: int = None) -> models.Order:
    """
    This helper function used to find a specific order
    *Args:
        order_id (int): the order id needed to be found
        db (Session): a database session
        coffee_shop_id (int): id of the coffee shop to find the order for
    *Returns:
        the found order if it exists, raise ShopsAppException otherwise
    """
    if not coffee_shop_id:
        found_order = db.query(models.Order).filter(models.Order.id == order_id).first()

    else:
        found_order = (
            db.query(models.Order)
            .filter(
                models.Order.id == order_id,
                models.Order.customer_id == models.Customer.id,
                models.Customer.coffee_shop_id == coffee_shop_id,
            )
            .first()
        )
    if not found_order:
        raise ShopsAppException(
            message=f"This order with id ={order_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return found_order


def find_all_orders(
    db: Session, coffee_shop_id: int, status: str = None
) -> list[models.Order]:
    """
    This helper function used to find all orders in the coffee_shop with specific status
    *Args:
        db (Session): a database session
        coffee_shop_id (int): id of the coffee shop to find the orders for
        status (str): the status of the orders to find

    *Returns:
        a list of all orders in the coffee_shop
    """
    if not status:
        return (
            db.query(models.Order)
            .filter(
                models.Order.customer_id == models.Customer.id,
                models.Customer.coffee_shop_id == coffee_shop_id,
            )
            .all()
        )
    return (
        db.query(models.Order)
        .filter(
            models.Order.status == status,
            models.Order.customer_id == models.Customer.id,
            models.Customer.coffee_shop_id == coffee_shop_id,
        )
        .all()
    )


def get_order_details(
    db: Session,
    coffee_shop_id: int,
    order_id: int = None,
    found_order: models.Order = None,
) -> schemas.OrderGETResponse:
    """
    This helper function used to get the order along with its details
    *Args:
        order_id (int): the order id needed to be found
        db (Session): a database session
        coffee_shop_id (int): id of the coffee shop to find the order for
        found_order (optional Order): this is the order object needed to obtain its details, it is optional
        if the order was found before calling this function
    *Returns:
        OrderGETResponse instance contains the order details
    """
    if not found_order and order_id is not None:
        found_order = find_order(
            order_id=order_id, coffee_shop_id=coffee_shop_id, db=db
        )

    order_items: list[schemas.MenuItemInGETOrderResponseBody] = [
        schemas.MenuItemInGETOrderResponseBody(
            id=order_item.item_id,
            quantity=order_item.quantity,
        )
        for order_item in db.query(models.OrderItem)
        .filter(models.OrderItem.order_id == found_order.id)
        .all()
    ]

    customer_phone_no = customer.get_customer_phone_no(
        db=db, customer_id=found_order.customer_id
    )
    return schemas.OrderGETResponse(
        id=found_order.id,
        status=found_order.status,
        order_items=order_items,
        issue_date=found_order.issue_date,
        issuer_id=found_order.issuer_id,
        customer_phone_no=customer_phone_no,
    )


def get_all_orders_details(
    status: str, db: Session, coffee_shop_id: int
) -> list[schemas.OrderGETResponse]:
    """
    This helper function used to get all orders along with their details
    *Args:
        status (str): the status of the orders needed to be retrieved
        db (Session): a database session
        coffee_shop_id (int): id of the coffee shop to find the order for
    *Returns:
        OrderGETResponse instance contains the order details
    """

    all_orders = find_all_orders(db=db, status=status, coffee_shop_id=coffee_shop_id)
    all_orders_with_details: list[schemas.OrderGETResponse] = [
        get_order_details(db=db, coffee_shop_id=coffee_shop_id, found_order=order)
        for order in all_orders
    ]
    return all_orders_with_details


def validate_status_change(new_status: OrderStatus, user_role: UserRole) -> None:
    """
    This helper function used to validate the change in the status of the order
    *Args:
        new_status (OrderStatus): the new status of the order
        user_role (UserRole): the role of the user who tries to change the statu
    *Returns:
        raise a ShopsAppException in case of violation
    """
    role_status_mapping = {
        UserRole.CASHIER: [OrderStatus.CLOSED],
        UserRole.CHEF: [OrderStatus.IN_PROGRESS, OrderStatus.COMPLETED],
    }

    if new_status not in role_status_mapping[user_role]:
        raise ShopsAppException(
            message="Unacceptable change of the status",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def update_order_status(
    request: schemas.OrderStatusPATCHRequestBody,
    order_id: int,
    user_role: UserRole,
    coffee_shop_id: int,
    user_id: int,
    db: Session,
) -> None:
    """
    This helper function used to update an order status, it applies conditions on
    the new status of the order along with the role of the user who
    tries to change this status
    *Args:
        request (schemas.OrderStatusPATCHRequestBody): the request body which contains the new status
        order_id (int): the order id needed to be changed
        coffee_shop_id (int): id of the coffee shop to find the order for
        user_role (UserRole): the role of the user needs to update the order's status
        db (Session): a database session
    *Returns:
        None in case of success, raise ShopsAppException in case of any failure
    """
    found_order = find_order(order_id=order_id, coffee_shop_id=coffee_shop_id, db=db)
    validate_status_change(new_status=request.status, user_role=user_role)
    found_order.status = request.status
    db.commit()


def assign_order(
    order_id: int,
    chef_id: int,
    coffee_shop_id: int,
    db: Session,
) -> None:
    """
    This helper function used to assign a specific order to a specific chef
    *Args:
        order_id (int): the order id needed to be assigned
        chef_id (int): the chef id needed to be assigned to
        coffee_shop_id(int): the coffee shop id of the user and the order
        db (Session): a database session
    *Returns:
        None in case of success, raise ShopsAppException in case of any failure
    """
    found_user = user.find_user(user_id=chef_id, db=db, coffee_shop_id=coffee_shop_id)
    if found_user.role != UserRole.CHEF:
        raise ShopsAppException(
            message="The assigner must be a chef",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    found_order = find_order(order_id=order_id, db=db, coffee_shop_id=coffee_shop_id)
    found_order.assigner_id = found_user.id
    db.commit()
