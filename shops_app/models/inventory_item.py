from shops_app.settings.database import Base
from sqlalchemy import (Column, Integer, String, ForeignKey,
                        DOUBLE_PRECISION, Boolean, DATE)


class InventoryItem(Base):
    """
    SQLAlchemy model for inventory items table
    """
    __tablename__ = 'inventory_item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(DOUBLE_PRECISION)
    expire_date = Column(DATE)
    prod_date = Column(DATE)
    available_quantity = Column(Integer)
    deleted = Column(Boolean, default=False)
    # relationship with users (inventory manager (admin))
    inventory_manager_id = Column(Integer, ForeignKey('users.id'))


