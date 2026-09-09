from sqlalchemy.orm import Session
from dataaccess.models import Order, Item

class OrdersRepository:
    def __init__(self,db: Session):
        self.db = db
    
    def create_order(self, order):
        
        item =(
            self.db.query(Item)
            .filter(Item.id == order.item_id)
            .first()
        )
        
        if item is None:
            return None
        
        total_price = item.price * order.quantity
        
        new_order = Order(
            user_id = order.user_id,
            restaurant_id = order.restaurant_id,
            item_id = order.item_id,
            quantity = order.quantity,
            total_price = total_price,
            order_status = "placed"
        )
        self.db.add(new_order)
        self.db.commit()
        self.db.refresh(new_order)
        return new_order
        
    def get_all_orders(self):
        return self.db.query(Order).all()
    
    def get_order_by_id(self, id: int):
        return self.db.query(Order).filter(Order.id == id).first()
    
    def get_orders_by_user_id(self, user_id: str):
        return self.db.query(Order).filter(Order.user_id == user_id).all()

    def get_orders_by_restaurant_id(self, restaurant_id: int):
        return self.db.query(Order).filter(Order.restaurant_id == restaurant_id).all()
    
    def get_orders_by_item_id(self, item_id: int):
        return self.db.query(Order).filter(Order.item_id == item_id).all()
    
    def update_order_status(self, id: int, status: str):
        db_order = (
            self.db.query(Order).filter(Order.id == id).first())
        
        if db_order is None:
            return None

        db_order.order_status = status
        
        self.db.commit()
        self.db.refresh(db_order)
        
        return db_order

    def delete_order_by_id(self, id: int):
        db_order = (
            self.db.query(Order).filter(Order.id == id).first())
        
        if db_order is None:
            return None
        
        self.db.delete(db_order)
        self.db.commit()
        
        return db_order 
        
    def order_statistics(self,db: Session):
        total_orders = self.db.query(Order).count()
        delivered_count = self.db.query(Order).filter(Order.order_status == "delivered").count()
        cancelled_count = self.db.query(Order).filter(Order.order_status == "cancelled").count()
        pending_count = self.db.query(Order).filter(Order.order_status == "pending").count()
        return {
            "total_orders":total_orders,
            "delivered_count":delivered_count,
            "cancelled_count":cancelled_count,
            "pending_count": pending_count
            }
    
