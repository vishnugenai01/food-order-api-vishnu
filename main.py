from fastapi import FastAPI, HTTPException, Depends
from database import SessionLocal, engine, Base
import models
from schemas import ItemCreate, ItemResponse
from sqlalchemy.orm import Session

app = FastAPI(title="Food Ordering API")

Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Endpoint 1 - Add menu item
@app.post("/menu", response_model=ItemResponse)
def add_menu_item(item: ItemCreate, db: Session = Depends(get_db)):

    new_item = models.Item(
        name=item.name,
        price=item.price,
        category=item.category,
        in_stock=item.in_stock
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

# Endpoint 2 - List all menu items
@app.get("/menu", response_model=list[ItemResponse])
def list_all_items(db: Session = Depends(get_db)):

    items = db.query(models.Item).all()

    if not items:
        raise HTTPException(
            status_code=404,
            detail="No menu items found"
        )

    return items

# Endpoint 3 - Get menu item by ID
@app.put("/menu/{item_id}", response_model=ItemResponse)
def update_menu_item(
    item_id: int,
    item: ItemCreate,
    db: Session = Depends(get_db)
):

    existing_item = db.query(models.Item).filter(
        models.Item.id == item_id
    ).first()

    if existing_item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    existing_item.name = item.name
    existing_item.price = item.price
    existing_item.category = item.category
    existing_item.in_stock = item.in_stock

    db.commit()
    db.refresh(existing_item)

    return existing_item

# Endpoint 4 - Delete menu item
@app.delete("/menu/{item_id}")
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(models.Item).filter(
        models.Item.id == item_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Menu item deleted successfully"
    }