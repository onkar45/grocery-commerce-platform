from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category")
