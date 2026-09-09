from sqlalchemy.orm import Session
from dataaccess.models import Item

class ItemRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_Item(self, item):
        new_item = Item(
            name = item.name,
            price = item.price,
            dietary_tags = item.dietary_tags,
            category = item.category,
            in_stock = item.in_stock,
            rating = item.rating,
            restaurant_id = item.restaurant_id,            
        )
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item
    
    def get_all_items(self) -> list[Item]:
        return self.db.query(Item).all()
    
    def get_item_by_id(self, id: int) -> Item:
        return self.db.query(Item).filter(Item.id == id).first()
    
    def get_items_by_restaurant_id(self, restaurant_id: int) -> list[Item]:
        return self.db.query(Item).filter(Item.restaurant_id == restaurant_id).all()

    def get_items_by_category(self, category: str) -> list[Item]:
        return self.db.query(Item).filter(Item.category == category).all()
    
    def get_items_by_rating(self, rating: float) -> list[Item]:
        return self.db.query(Item).filter(Item.rating == rating).all()

    def get_items_by_dietary_tags(self, dietary_tags: str) -> list[Item]:
        return self.db.query(Item).filter(Item.dietary_tags == dietary_tags).all()

    def update_item_by_id(self, id: int, item):
        db_item = (
            self.db.query(Item).filter(Item.id == id).first())
        
        if db_item is None:
            return None
        
        db_item.name = item.name
        db_item.price = item.price
        db_item.dietary_tags = item.dietary_tags
        db_item.category = item.category
        db_item.in_stock = item.in_stock
        db_item.rating = item.rating
        db_item.restaurant_id = item.restaurant_id
        
        self.db.commit()
        self.db.refresh(db_item)
        
        return db_item
    
    def delete_item_by_id(self, id: int):
        db_item = (
            self.db.query(Item).filter(Item.id == id).first())
        
        if db_item is None:
            return None
        self.db.delete(db_item)
        self.db.commit()
        
        return db_item