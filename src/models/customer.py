from src.settings.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Customer(Base):
    """
    SQLAlchemy model for Customer table
    """

    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_no = Column(String, unique=True, nullable=False)
    coffee_shop_id = Column(Integer, ForeignKey("coffee_shop.id"))
    deleted = Column(Boolean, default=False)
