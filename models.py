from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, default="veg")
    in_stock = Column(Boolean, default=True)
    
class Order(Base):
    __tablename__ = "Orders"
    
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    order_status = Column(String, default="pending") # pending, completed, cancelled