from shops_app.settings.database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Customer(Base):
    """
    SQLAlchemy model for Customer table
    """
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_no = Column(String, unique=True, nullable=False)
    deleted = Column(Boolean, default=False)



