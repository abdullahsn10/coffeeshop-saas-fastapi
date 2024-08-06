from shops_app.settings.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Branch(Base):
    """
    SQLAlchemy model for Branch table
    """
    __tablename__ = 'branches'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    deleted = Column(Boolean, default=False)
    # relationship with coffee shops
    coffee_shop_id = Column(Integer, ForeignKey('coffee_shops.id'))
