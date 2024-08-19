from pydantic import BaseModel
from src.schemas.menu_item import (
    MenuItemInPOSTOrderRequestBody,
    MenuItemInGETOrderResponseBody,
)
from src.schemas.customer import CustomerPOSTRequestBody
from src.models.order import OrderStatus
from datetime import datetime


class OrderPOSTRequestBody(BaseModel):
    """
    pydantic schema for the order in POST request body
    """

    customer_details: CustomerPOSTRequestBody
    order_items: list[MenuItemInPOSTOrderRequestBody]


class OrderPOSTResponse(BaseModel):
    """
    pydantic schema for the order in POST response body
    """

    id: int
    customer_phone_no: str
    status: OrderStatus


class OrderGETResponse(BaseModel):
    """
    pydantic schema for the order in GET response body
    """

    id: int
    issue_date: datetime
    issuer_id: int
    status: OrderStatus
    phone_no: str
    items: list[MenuItemInGETOrderResponseBody]

    class Config:
        orm_mode = True
        from_attributes = True


class OrderStatusPATCHRequestBody(BaseModel):
    """
    pydantic schema for the order Status in PATCH request body
    """

    status: OrderStatus


class PaginatedOrderResponse(BaseModel):
    """
    pydantic schema for the paginated orders in GET response body
    """

    total_count: int
    page: int
    page_size: int
    orders: list[OrderGETResponse]
