from shops_app.settings.database import Base
from sqlalchemy import (Column, Integer, String, Boolean,
                        Enum as SQLAlchemyEnum, ForeignKey)
from enum import Enum


class UserRole(Enum):
    """
    Enum class to represent the role of a user.
    'cashier', 'chef', 'order_receiver', 'admin'
    """
    ADMIN = 'admin'
    CASHIER = 'cashier'
    CHEF = 'chef'
    ORDER_RECEIVER = 'order_receiver'


class User(Base):
    """
    SQLAlchemy model to represent a user.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone_no = Column(String, unique=True)
    password = Column(String)
    deleted = Column(Boolean, default=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
    # relationship with branch (belongs to)
    branch_id = Column(Integer, ForeignKey('branches.id'))


