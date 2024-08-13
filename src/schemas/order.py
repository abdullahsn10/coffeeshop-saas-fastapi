from pydantic import BaseModel
from src.schemas.menu_item import MenuItemInPOSTOrderRequestBody
from src.schemas.customer import CustomerPOSTRequestBody
from src.models.order import OrderStatus


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
