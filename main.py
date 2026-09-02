from fastapi import FastAPI, HTTPException, Depends
from database import SessionLocal, engine, Base
import models
from schemas import ItemCreate, ItemResponse, OrderCreate, OrderResponse, OrderStatusUpdate, RestaurantCreate, RestaurantResponse
from sqlalchemy.orm import Session
from memory import save_message, get_messages

app = FastAPI(title="Food Ordering API")

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
@app.post("/messages/{user_id}")
def add_message(
    user_id: str,
    role: str,
    content: str,
    db: Session = Depends(get_db)
):

    save_message(db, user_id, role, content)

    return {
        "message": "Message saved successfully"
    }
    
@app.get("/messages/{user_id}")
def fetch_messages(
    user_id: str,
    db: Session = Depends(get_db)
):

    return get_messages(db, user_id)

#Endpoint 1 - Add Restaurant
@app.post(
    "/restaurants",
    response_model=RestaurantResponse
)
def add_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db)
):

    new_restaurant = models.Restaurant(
        name=restaurant.name,
        location=restaurant.location
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant

# Endpoint 2 - Get all restaurants
@app.get(
    "/restaurants/list",
    response_model=list[RestaurantResponse]
)
def get_all_restaurants(
    db: Session = Depends(get_db)
):
    restaurants = db.query(models.Restaurant).all()

    if not restaurants:
        raise HTTPException(
            status_code=404,
            detail="No restaurants found"
        )

    return restaurants

# Endpoint 3 - Add menu item to a restaurant
@app.post(
    "/restaurants/{restaurant_id}/menu",
    response_model=ItemResponse
)
def add_restaurant_menu_items(
    restaurant_id: int,
    item: ItemCreate,
    db: Session = Depends(get_db)
):

    restaurant = db.query(models.Restaurant).filter(
        models.Restaurant.id == restaurant_id
    ).first()

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    new_item = models.Item(
        name=item.name,
        price=item.price,
        dietary_tags=item.dietary_tags,
        category=item.category,
        in_stock=item.in_stock,
        rating=item.rating,
        restaurant_id=restaurant_id
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

# Endpoint 4 - Get menu of a restaurant
@app.get(
    "/restaurants/{restaurant_id}/menu",
    response_model=list[ItemResponse]
)
def get_restaurant_menu(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

    restaurant = db.query(models.Restaurant).filter(
        models.Restaurant.id == restaurant_id
    ).first()

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    items = db.query(models.Item).filter(
        models.Item.restaurant_id == restaurant_id
    ).all()

    if not items:
        raise HTTPException(
            status_code=404,
            detail="No menu items found for this restaurant"
        )

    return items

# Endpoint 5 - Get best rated food
@app.get(
    "/menu/best/rated/{restaurant_id}",
    response_model=list[ItemResponse]
)
def get_best_items(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = db.query(models.Restaurant).filter(
        models.Restaurant.id == restaurant_id
    ).first()
    
    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )
    print("Restaurant ID received:", restaurant_id)
    items = db.query(models.Item).filter(
        models.Item.restaurant_id == restaurant_id,
        models.Item.in_stock == True,
        models.Item.rating > 4
    ).order_by(
        models.Item.rating.desc()
    ).all()

    if not items:
        raise HTTPException(
            status_code=404,
            detail="No menu items found"
        )

    return items

# Endpoint 6 - Filter menu by dietary_tag
@app.get("/restaurants/{restaurant_id}/menu/dietary_tag/{dietary_tag}", response_model=list[ItemResponse])
def get_items_by_dietary_tag(
    restaurant_id: int,
    dietary_tag: str,
    db: Session = Depends(get_db)
):

    items = db.query(models.Item).filter(
        models.Item.restaurant_id == restaurant_id,
        models.Item.dietary_tags.ilike(dietary_tag)
    ).all()

    if not items:
        raise HTTPException(
            status_code=404,
            detail=f"No items found in category '{dietary_tag}'"
        )

    return items

# Endpoint 7 - update menu item by ID
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
    existing_item.dietary_tags = item.dietary_tags
    existing_item.category = item.category
    existing_item.in_stock = item.in_stock
    existing_item.rating = item.rating

    db.commit()
    db.refresh(existing_item)

    return existing_item

# Endpoint 8 - Delete menu item
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
        
    existing_order = db.query(models.Order).filter(
        models.Order.item_id == item_id
    ).first()
    
    if existing_order is not None:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete item because it is present in  order"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Menu item deleted successfully"
    }
    
# Endpoint 9 - Place an order
@app.post("/orders", response_model=OrderResponse)
def place_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    restaurant = db.query(models.Restaurant).filter(
        models.Restaurant.id == order.restaurant_id
    ).first()
    
    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail=f"Restaurant {order.restaurant_id} not found"
        )

    item = db.query(models.Item).filter(
        models.Item.id == order.item_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item {order.item_id} not found"
        )

    if not item.in_stock:
        raise HTTPException(
            status_code=400,
            detail=f"{item.name} is out of stock"
        )

    total_price = item.price * order.quantity

    new_order = models.Order(
            user_id=order.user_id,
            restaurant_id=order.restaurant_id,
            item_id=order.item_id,
            quantity=order.quantity,
            total_price=total_price,
            order_status="placed"
        )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "id": new_order.id,
        "user_id": new_order.user_id,
        "item_name": item.name,
        "item_id": new_order.item_id,
        "quantity": new_order.quantity,
        "total_price": new_order.total_price,
        "order_status": new_order.order_status
    }

# Endpoint 10 - Get Order statistics
@app.get("/orders/stats")
def order_statistics(
    db: Session = Depends(get_db)
):

    total_orders = db.query(models.Order).count()

    delivered_orders = db.query(models.Order).filter(
        models.Order.order_status == "delivered"
    ).count()

    orders = db.query(models.Order).all()

    total_revenue = sum(
        order.total_price
        for order in orders
        if order.order_status == "delivered"
    )

    return {
        "total_orders": total_orders,
        "delivered_count": delivered_orders,
        "total_revenue": total_revenue
    }
    
# Endpoint 11 - Get orders for a particular user
@app.get("/orders/user/{user_id}")
def get_user_orders(
    user_id: int,
    db: Session = Depends(get_db)
):
    orders = (
        db.query(models.Order)
        .filter(models.Order.user_id == user_id)
        .all()
    )

    if not orders:
        raise HTTPException(
            status_code=404,
            detail=f"No orders found for user {user_id}"
        )

    result = []

    for order in orders:

        item = db.query(models.Item).filter(
            models.Item.id == order.item_id
        ).first()

        result.append({
            "id": order.id,
            "user_id": order.user_id,
            "item_name": item.name if item else "Unknown item",
            "item_id": order.item_id,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "order_status": order.order_status
        })

    return result


# Endpoint 12 - Get order details
@app.get("/orders/{order_id}/user/{user_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    user_id: int,   
    db: Session = Depends(get_db)
):

    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == user_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"No Order {order_id} found for user {user_id}"
        )
    item = db.query(models.Item).filter(
        models.Item.id == order.item_id
    ).first()
    
    if item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item {order.item_id} not found"
        )

    return {
        "id": order.id,
        "user_id": order.user_id,
        "item_name": item.name,
        "item_id": order.item_id,
        "quantity": order.quantity,
        "total_price": order.total_price,
        "order_status": order.order_status
    }

# Endpoint 13 - Update order status
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

    current_status = order.order_status
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

    order.order_status = new_status

    db.commit()
    db.refresh(order)

    return {
        "message": "Order status updated successfully",
        "order_id": order.id,
        "status": order.order_status
    }
    
# Endpoint 14 - Cancel an order
@app.delete("/orders/{order_id}")
def cancel_order(
    order_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == user_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"No Order {order_id} found for user {user_id}"
        )

    if order.order_status != "placed":
        raise HTTPException(
            status_code=400,
            detail="Order can only be cancelled when status is 'placed'"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order cancelled successfully"
    }
    

