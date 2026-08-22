from pydantic import BaseModel


class ItemCreate(BaseModel):
    id: int
    name: str
    price: float
    category: str = "veg" or "Non-veg"
    in_stock: bool = True


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
    in_stock: bool

    class Config:
        from_attributes = True
        
class OrderCreate(BaseModel):
    item_name: str
    quantity: int
                
class OrderResponse(BaseModel):
    id: int
    item_name: str
    quantity: int
    total_price: float
    order_status: str
    
    class Config:
            from_attributes = True

        
class OrderStatusUpdate(BaseModel):
    status: str 
    
    class Config:
        from_attributes = True
        
