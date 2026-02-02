from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    module = Column(String(50), nullable=False)
