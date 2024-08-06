from shops_app.settings.database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Customer(Base):
    """
    SQLAlchemy model for Customer table
    """
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_no = Column(String, unique=True)
    deleted = Column(Boolean, default=False)



