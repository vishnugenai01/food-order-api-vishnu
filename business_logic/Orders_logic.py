from sqlalchemy.orm import Session
from fastapi import HTTPException
from dataaccess.repository.Orders import OrdersRepository

class OrdersLogic:
    def __init__(self, db: Session):
        self.db = db
        self.Order_repo = OrdersRepository(db)

    def create_order(self, order):
        try:
            db_result = self.Order_repo.create_order(order)
            
            if db_result is None:
                raise HTTPException(status_code=404, detail="Item not found")
            return db_result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_all_orders(self):
        try:
            db_result = self.Order_repo.get_all_orders()
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_order_by_id(self, id: int):
        try:
            db_result = self.Order_repo.get_order_by_id(id)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_orders_by_user_id(self, user_id: str):
        try:
            db_result = self.Order_repo.get_orders_by_user_id(user_id)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_orders_by_restaurant_id(self, restaurant_id: int):
        try:
            db_result = self.Order_repo.get_orders_by_restaurant_id(restaurant_id)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_orders_by_item_id(self, item_id: int):
        try:
            db_result = self.Order_repo.get_orders_by_item_id(item_id)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def update_order_status(self, id: int, status: str):
        try:
            db_result = self.Order_repo.update_order_status(id, status)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def delete_order_by_id(self, id: int):
        try:
            db_result = self.Order_repo.delete_order_by_id(id)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_order_statistics(self):
        try:
            db_result = self.Order_repo.get_order_statistics()
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))