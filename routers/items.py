from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routers.models import ItemCreate, ItemResponse
from config.session import get_db
from business_logic.items_logic import ItemsLogic


router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.post("/", response_model=ItemResponse)
async def create_Item(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        service_logic = ItemsLogic(db=db)
        
        service_response = service_logic.create_Item(item=item)
        return service_response
    except Exception as e:
        print("CREATE ITEM ERROR:", repr(e))
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ItemResponse])
async def get_all_items(db: Session = Depends(get_db)):
    service_logic = ItemsLogic(db=db)

    service_response = service_logic.get_all_items()
    return service_response
    
@router.get("/restaurant/{restaurant_id}", response_model=list[ItemResponse])
async def get_items_by_restaurant_id(restaurant_id: int, db: Session = Depends(get_db)):
    service_logic = ItemsLogic(db=db)

    service_response = service_logic.get_items_by_restaurant_id(restaurant_id=restaurant_id)
    return service_response
    

@router.get("/category/{category}", response_model=list[ItemResponse])
async def get_items_by_category(category: str, db: Session = Depends(get_db)):
    service_logic = ItemsLogic(db=db)

    service_response = service_logic.get_items_by_category(category=category)
    return service_response

@router.get("/rating/{rating}", response_model=list[ItemResponse])
async def get_items_by_rating(rating: int, db: Session = Depends(get_db)):
    service_logic = ItemsLogic(db=db)

    service_response = service_logic.get_items_by_rating(rating=rating)
    return service_response

@router.get("/dietary/{dietary_tag}", response_model=list[ItemResponse])
async def get_items_by_dietary_tags(dietary_tag: str, db: Session = Depends(get_db)):
    service_logic = ItemsLogic(db=db)

    service_response = service_logic.get_items_by_dietary_tags(dietary_tag=dietary_tag)
    return service_response

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    service_logic = ItemsLogic(db=db)

    service_response = service_logic.get_item_by_id(item_id)
    if service_response is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    return service_response
    
@router.put("/{item_id}", response_model=ItemResponse)
async def update_item_by_id(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    service_logic = ItemsLogic(db=db)

    service_response = service_logic.update_item_by_id(item_id, item)
    if service_response is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return service_response


@router.delete("/{item_id}")
async def delete_item_by_id(item_id: int, db: Session = Depends(get_db)):
    service_logic = ItemsLogic(db=db)

    service_response = service_logic.delete_item_by_id(item_id)
    if service_response is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return{
        "message": f"Item {item_id} deleted successfully"
    }