from pydantic import BaseModel


class CustomerOrderReport(BaseModel):
    """
    pydantic model for customer order report
    """

    id: int
    name: str
    phone_no: str
    total_orders: int
    total_paid: float

    class Config:
        orm_mode = True


class ChefOrderReport(BaseModel):
    """
    pydantic model for chef order report
    """

    id: int
    chef_name: str
    served_orders: int

    class Config:
        orm_mode = True


class IssuerOrderReport(BaseModel):
    """
    pydantic model for issuer order report
    """

    id: int
    issuer_name: str
    issued_orders: int

    class Config:
        orm_mode = True
