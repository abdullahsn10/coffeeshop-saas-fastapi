from src.settings.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class OrderItem(Base):
    """
    SQLAlchemy model for OrderItem relationship table between
    users table and the menu_items table
    """

    __tablename__ = "order_item"

    # relationship attribute (many-many between order and menu items table)
    order_id = Column(Integer, ForeignKey("order.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("menu_item.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
