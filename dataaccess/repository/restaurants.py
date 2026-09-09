from sqlalchemy.orm import Session
from dataaccess.models import Restaurant

class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_restaurant(self, restaurant: Restaurant, db: Session):
        new_restaurant = Restaurant(
            name = restaurant.name,
            location = restaurant.location,
        )
        self.db.add(new_restaurant)
        self.db.commit()
        self.db.refresh(new_restaurant)
        return new_restaurant
    
    def get_all_restaurants(self) -> list[Restaurant]:
        return self.db.query(Restaurant).all()
    
    def get_restaurant_by_id(self, id: int) -> Restaurant:
        return self.db.query(Restaurant).filter(Restaurant.id == id).first()

    def get_restaurants_by_location(self, location: str) -> list[Restaurant]:
        return self.db.query(Restaurant).filter(Restaurant.location == location).all()
