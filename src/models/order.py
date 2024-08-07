from datetime import datetime
from src.settings.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey


class Order(Base):
    """
    SQLAlchemy model for orders
    """

    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    issue_date = Column(TIMESTAMP, nullable=False, default=datetime.now)
    # relationship with customers table (customer of the order)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    # relationship with users table (employee who placed the order)
    employee_id = Column(Integer, ForeignKey("user.id"), nullable=False)