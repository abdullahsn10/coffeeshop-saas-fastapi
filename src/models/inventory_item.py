from src.settings.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DOUBLE_PRECISION,
    Boolean,
    DATE,
)


class InventoryItem(Base):
    """
    SQLAlchemy model for inventory items table
    """

    __tablename__ = "inventory_item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(DOUBLE_PRECISION, nullable=False)
    expire_date = Column(DATE)
    prod_date = Column(DATE)
    available_quantity = Column(Integer, nullable=False)
    deleted = Column(Boolean, default=False)
    # relationship with Coffee Shop
    coffee_shop_id = Column(Integer, ForeignKey("coffee_shop.id"))
