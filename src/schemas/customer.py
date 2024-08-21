from pydantic import BaseModel


class CustomerPOSTRequestBody(BaseModel):
    """
    Pydantic schema for Customer in POST request body
    """

    name: str
    phone_no: str


class CustomerPUTRequestBody(CustomerPOSTRequestBody):
    """
    Pydantic schema for Customer in PUT request body
    """

    pass


class CustomerResponse(BaseModel):
    """
    Pydantic schema for Customer response
    """

    id: int
    name: str
    phone_no: str
    coffee_shop_id: int

    class Config:
        orm_mode = True
        from_attributes = True
