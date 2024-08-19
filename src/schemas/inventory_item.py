from datetime import date

from pydantic import BaseModel


class InventoryItemPOSTRequestBody(BaseModel):
    """
    pydantic schema for InventoryItem in POST RequestBody
    """

    name: str
    price: float
    expire_date: date
    prod_date: date
    available_quantity: int


class InventoryItemGETResponse(BaseModel):
    """
    pydantic schema for InventoryItem in Response of any HTTP request
    """

    id: int
    name: str
    price: float
    expire_date: date
    prod_date: date
    available_quantity: int


class InventoryItemPUTRequestBody(InventoryItemPOSTRequestBody):
    """
    pydantic schema for InventoryItem in PUT RequestBody
    """

    pass


class InventoryItemPOSTResponse(InventoryItemGETResponse):
    """
    pydantic schema for InventoryItem in POST Response
    """

    class Config:
        orm_mode = True


class InventoryItemPUTResponse(InventoryItemGETResponse):
    """
    pydantic schema for InventoryItem in PUT Response
    """

    class Config:
        orm_mode = True
