from pydantic import BaseModel

class RestaurantCreate(BaseModel):
    name: str
    location: str
    
class RestaurantResponse(BaseModel):
    id: int
    name: str
    location: str
    
    class Config:
        from_attributes = True

class ItemCreate(BaseModel):
    name: str
    price: float
    dietary_tags: str = "veg" or "Non-veg"
    category: str
    in_stock: bool = True
    rating: float = 0.0


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    dietary_tags: str
    category: str
    in_stock: bool
    rating: float
    restaurant_id: int

    class Config:
        from_attributes = True
        
class OrderCreate(BaseModel):
    restaurant_id: int
    item_id: int
    quantity: int
                
class OrderResponse(BaseModel):
    id: int
    item_name: str
    item_id: int
    quantity: int
    total_price: float
    order_status: str
    
    class Config:
            from_attributes = True

        
class OrderStatusUpdate(BaseModel):
    status: str 
    
    class Config:
        from_attributes = True
        
