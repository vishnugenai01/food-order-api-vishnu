from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    dietary_tags = Column(String, default="veg")
    category = Column(String)
    in_stock = Column(Boolean, default=True)
    rating = Column(Float, default=0.0)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    restaurant = relationship("Restaurant", back_populates="items")
    
class Order(Base):
    __tablename__ = "orders"    
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    order_status = Column(String, default="pending") # pending, completed, cancelled
    
class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    items = relationship("Item", back_populates="restaurant", cascade="all, delete")
    
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)