from sqlalchemy.orm import Session
from fastapi import HTTPException
from dataaccess.repository.restaurants import RestaurantRepository

class RestaurantsLogic:
    def __init__(self, db: Session):
        self.db = db
        self.restaurant_repo = RestaurantRepository(db)

    def create_restaurant(self, restaurant):
        try:
            db_result = self.restaurant_repo.create_restaurant(restaurant)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_all_restaurants(self):
        try:
            db_result = self.restaurant_repo.get_all_restaurants()
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_restaurant_by_id(self, id: int):
        try:
            db_result = self.restaurant_repo.get_restaurant_by_id(id)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_restaurants_by_location(self, location: str):
        try:
            db_result = self.restaurant_repo.get_restaurants_by_location(location)
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

