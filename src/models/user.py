from src.settings.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Enum as SQLAlchemyEnum,
    ForeignKey,
)
from enum import Enum


class UserRole(Enum):
    """
    Enum class to represent the role of a user.
    'cashier', 'chef', 'order_receiver', 'admin'
    """

    ADMIN = "ADMIN"
    CASHIER = "CASHIER"
    CHEF = "CHEF"
    ORDER_RECEIVER = "ORDER_RECEIVER"


class User(Base):
    """
    SQLAlchemy model to represent a user.
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_no = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    deleted = Column(Boolean, default=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
    # relationship with branch (belongs to)
    branch_id = Column(Integer, ForeignKey("branch.id"))
