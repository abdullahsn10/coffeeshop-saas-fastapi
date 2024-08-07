from src.settings.database import Base
from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey,
                        DOUBLE_PRECISION)


class MenuItem(Base):
    """
    SQLAlchemy model for MenuItem table
    """
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(DOUBLE_PRECISION, nullable=False)
    deleted = Column(Boolean, default=False)

