from pydantic import BaseModel


class CoffeeShopBase(BaseModel):
    """
    Pydantic schema for CoffeeShop, it includes all coffee shop details
    except the id
    """

    name: str
    location: str
    contact_info: str

    class Config:
        orm_mode = True


class CoffeeShopResponse(CoffeeShopBase):
    """
    Pydantic schema for CoffeeShop, it includes all coffee shop details
    """

    class Config:
        orm_mode = True
