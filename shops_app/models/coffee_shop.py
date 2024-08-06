from shops_app.settings.database import Base
from sqlalchemy import Column, Integer, String


class CoffeeShop(Base):
    """
    SQLAlchemy model for Coffee Shop table
    """
    __tablename__ = 'coffee_shops'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    contact_info = Column(String)
