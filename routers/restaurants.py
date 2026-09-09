from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routers.models import RestaurantCreate, RestaurantResponse
from config.session import get_db
from business_logic.restaurants_logic import RestaurantsLogic

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
)

@router.post("/", response_model=RestaurantResponse)
async def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    try:
        service_logic = RestaurantsLogic(db=db)
        
        service_response = service_logic.create_restaurant(restaurant)
        return service_response
    except Exception as e:
        print("CREATE RESTAURANT ERROR:", repr(e))
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[RestaurantResponse])
async def get_all_restaurants(db: Session = Depends(get_db)):
    service_logic = RestaurantsLogic(db=db)
    
    service_response = service_logic.get_all_restaurants()
    return service_response

@router.get("/{id}", response_model=RestaurantResponse)
async def get_restaurant_by_id(id: int, db: Session = Depends(get_db)):
    service_logic = RestaurantsLogic(db=db)

    service_response = service_logic.get_restaurant_by_id(id)
    return service_response

@router.get("/location/{location}", response_model=list[RestaurantResponse])
async def get_restaurants_by_location(location: str, db: Session = Depends(get_db)):
    service_logic = RestaurantsLogic(db=db)

    service_response = service_logic.get_restaurants_by_location(location)
    return service_response
    