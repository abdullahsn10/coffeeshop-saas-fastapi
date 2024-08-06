from shops_app.settings.database import Base
from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey,
                        DOUBLE_PRECISION)


class MenuItem(Base):
    """
    SQLAlchemy model for MenuItem table
    """
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(DOUBLE_PRECISION)
    deleted = Column(Boolean, default=False)

