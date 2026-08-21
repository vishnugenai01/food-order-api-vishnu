from fastapi import FastAPI, HTTPException, Depends
from database import SessionLocal, engine, Base
import models
from schemas import ItemCreate, ItemResponse, OrderCreate, OrderResponse, OrderStatusUpdate
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
    
# Endpoint 5 - Filter menu by category
@app.get("/menu/category/{category}", response_model=list[ItemResponse])
def get_items_by_category(
    category: str,
    db: Session = Depends(get_db)
):

    items = db.query(models.Item).filter(
        models.Item.category == category
    ).all()

    if not items:
        raise HTTPException(
            status_code=404,
            detail=f"No items found in category '{category}'"
        )

    return items

# Endpoint 6 - Place an order
@app.post("/orders", response_model=OrderResponse)
def place_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    total_price = 0

    for order_item in order.items:

        item = db.query(models.Item).filter(
            models.Item.id == order_item.item_id
        ).first()

        if item is None:
            raise HTTPException(
                status_code=404,
                detail=f"Item {order_item.item_id} not found"
            )

        if not item.in_stock:
            raise HTTPException(
                status_code=400,
                detail=f"{item.name} is out of stock"
            )

        total_price += item.price * order_item.quantity

    new_order = models.Order(
        total_price=total_price,
        status="placed"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for order_item in order.items:

        new_order_item = models.OrderItem(
            order_id=new_order.id,
            item_id=order_item.item_id,
            quantity=order_item.quantity
        )

        db.add(new_order_item)

    db.commit()
    db.refresh(new_order)

    return new_order

# Endpoint 7 - Get order details
@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order

# Endpoint 8 - Update order status
@app.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):

    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    current_status = order.status
    new_status = status_data.status

    valid_statuses = [
        "placed",
        "preparing",
        "delivered"
    ]

    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid order status"
        )

    if current_status == "placed" and new_status not in [
        "preparing",
        "delivered"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status transition"
        )

    if current_status == "preparing" and new_status != "delivered":
        raise HTTPException(
            status_code=400,
            detail="Order can only move from preparing to delivered"
        )

    if current_status == "delivered":
        raise HTTPException(
            status_code=400,
            detail="Delivered order cannot be updated"
        )

    order.status = new_status

    db.commit()
    db.refresh(order)

    return {
        "message": "Order status updated successfully",
        "order_id": order.id,
        "status": order.status
    }
    
# Endpoint 9 - Cancel an order
@app.delete("/orders/{order_id}")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.status != "placed":
        raise HTTPException(
            status_code=400,
            detail="Order can only be cancelled when status is 'placed'"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order cancelled successfully"
    }