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


@app.get("/menu")
def menu():
    return "Welcome to Food Ordering API"


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


