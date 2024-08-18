from pydantic import BaseModel


class CustomerPOSTRequestBody(BaseModel):
    """
    Pydantic schema for Customer in POST request body
    """

    name: str
    phone_no: str
