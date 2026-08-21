from pydantic import BaseModel


class ItemCreate(BaseModel):
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
        
class OrderResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    total_price: float

class OrderCreate(BaseModel):
    name: str
    price: float
    category: str = "veg" or "Non-veg"
    in_stock: bool = True

    class Config:
        from_attributes = True
        
class OrderStatusUpdate(BaseModel):
    status: str = "placed" or "preparing" or "delivered"
    class Config:
        from_attributes = True
        
