from shops_app.settings.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class BranchUser(Base):
    """
    SQLAlchemy model for BranchUser relationship table
    """
    __tablename__ = 'branches_users'

    # relationship attributes
    branch_id = Column(Integer, ForeignKey('branches.id'), primary_key=True)
    manager_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
