from datetime import datetime
from src.settings.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    Enum as SQLAlchemyEnum,
)
from enum import Enum


class OrderStatus(Enum):
    """
    Enum class to represent the role of a user.
    'cashier', 'chef', 'order_receiver', 'admin'
    """

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"


class Order(Base):
    """
    SQLAlchemy model for orders
    """

    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    issue_date = Column(TIMESTAMP, nullable=False, default=datetime.now)
    # relationship with customers table (customer of the order)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    status = Column(SQLAlchemyEnum(OrderStatus), nullable=False)
    # relationship with users table (employee who placed the order)
    issuer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    # relationship with users table (employee(chef) who take the order)
    assigner_id = Column(Integer, ForeignKey("user.id"), nullable=True)
