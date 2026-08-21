from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    price: float
    category: str = "veg"
    in_stock: bool = True


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
    in_stock: bool

    class Config:
        from_attributes = True