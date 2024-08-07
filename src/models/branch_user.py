from src.settings.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class BranchUser(Base):
    """
    SQLAlchemy model for BranchUser relationship table
    """
    __tablename__ = 'branch_user'

    # relationship attributes
    branch_id = Column(Integer, ForeignKey('branch.id'), primary_key=True)
    manager_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
