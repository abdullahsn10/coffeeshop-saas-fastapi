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


class OrderPOSTResponseBody(BaseModel):
    """
    pydantic schema for the order in POST response body
    """

    id: int
    customer_phone_no: str
    status: OrderStatus


class OrderGETResponse(BaseModel):
    id: int
    issue_date: datetime
    issuer_id: int
    status: OrderStatus
    customer_phone_no: str
    order_items: list[MenuItemInGETOrderResponseBody]
