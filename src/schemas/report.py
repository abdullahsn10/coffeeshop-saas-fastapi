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
