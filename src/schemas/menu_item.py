from pydantic import BaseModel


class MenuItemPOSTRequestBody(BaseModel):
    """
    pydantic schema for MenuItem in POST request body
    """

    name: str
    description: str
    price: float


class MenuItemGETResponse(BaseModel):
    """
    pydantic schema for MenuItem in response of any HTTP request
    """

    id: int
    name: str
    description: str
    price: float


class MenuItemPUTRequestBody(MenuItemPOSTRequestBody):
    """
    pydantic schema for MenuItem in PUT request body
    """

    pass


class MenuItemInPOSTOrderRequestBody(BaseModel):
    """
    pydantic schema for MenuItem in In POST Order request body
    """

    id: int
    quantity: int
