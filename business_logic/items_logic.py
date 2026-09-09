from sqlalchemy.orm import Session
from fastapi import HTTPException
from dataaccess.repository.items import ItemRepository


class ItemsLogic:
    def __init__(self, db: Session):
        self.db = db
        self.item_repo = ItemRepository(self.db)
    
    def create_Item(self,item):
        try:
            db_result = self.item_repo.create_Item(item)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_all_items(self):
        try:
            db_result = self.item_repo.get_all_items()
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_item_by_id(self, id: int):
        try:
            db_result = self.item_repo.get_item_by_id(id)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_items_by_restaurant_id(self, restaurant_id: int):
        try:
            db_result = self.item_repo.get_items_by_restaurant_id(restaurant_id)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_items_by_category(self, category: str):
        try:
            db_result = self.item_repo.get_items_by_category(category)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_items_by_rating(self, rating: float):
        try:
            db_result = self.item_repo.get_items_by_rating(rating)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_items_by_dietary_tags(self, dietary_tag: str):
        try:
            db_result = self.item_repo.get_items_by_dietary_tags(dietary_tag)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    

    def update_item_by_id(self, id: int, item):
        try:
            db_result = self.item_repo.update_item_by_id(id, item)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_item_by_id(self, id: int):
        try:
            db_result = self.item_repo.delete_item_by_id(id)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))