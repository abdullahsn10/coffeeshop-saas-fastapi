from src.settings.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint


class Customer(Base):
    """
    SQLAlchemy model for Customer table
    """

    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_no = Column(String, nullable=False)
    coffee_shop_id = Column(Integer, ForeignKey("coffee_shop.id"))
    deleted = Column(Boolean, default=False)

    # adding uniqueness constraint for phone and coffee_shop
    __table_args__ = (
        UniqueConstraint("phone_no", "coffee_shop_id", name="unique_phone_shop"),
    )
