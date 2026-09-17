from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routers.models import OrderCreate, OrderResponse, OrderStatusUpdate
from config.session import get_db
from business_logic.Orders_logic import OrdersLogic

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.post("/orders/create", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        service_logic = OrdersLogic(db)
        
        service_response = service_logic.create_order(order)
        
        if service_response is None:
            raise HTTPException(status_code=500, detail="Item not found")
        return service_response
    except HTTPException:
        raise
    except Exception as e:
        print("Error in create_order:", repr(e))
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/all", response_model=list[OrderResponse])
async def get_all_orders(db: Session = Depends(get_db)):
    try:
        service_logic = OrdersLogic(db)

        service_response = service_logic.get_all_orders()
        return service_response
    except Exception as e:
        print("Error in get_all_orders:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/user/{user_id}", response_model=list[OrderResponse])
async def get_orders_by_user_id(user_id: str, db: Session = Depends(get_db)):
    try:
        service_logic = OrdersLogic(db)

        service_response = service_logic.get_orders_by_user_id(user_id)
        return service_response
    except Exception as e:
        print("Error in get_orders_by_user_id:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))   

@router.get("/restaurant/{restaurant_id}", response_model=list[OrderResponse])
async def get_orders_by_restaurant_id(restaurant_id: int, db: Session = Depends(get_db)):
    try:
        service_logic = OrdersLogic(db)

        service_response = service_logic.get_orders_by_restaurant_id(restaurant_id)
        return service_response
    except Exception as e:
        print("Error in get_orders_by_restaurant_id:", repr(e))
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/item/{item_id}", response_model=list[OrderResponse])
async def get_orders_by_item_id(item_id: int, db: Session = Depends(get_db)):
    try:
        service_logic = OrdersLogic(db)

        service_response = service_logic.get_orders_by_item_id(item_id)
        return service_response
    except Exception as e:
        print("Error in get_orders_by_item_id:", repr(e))
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    try:
        service_logic = OrdersLogic(db)

        service_response = service_logic.get_order_by_id(order_id)
        
        if service_response is None:
            raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
        return service_response
    except HTTPException:
        raise
    except Exception as e:
        print("Error in get_order_by_id:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: int, status: OrderStatusUpdate, db: Session = Depends(get_db)):
    try:
        service_logic = OrdersLogic(db)

        service_response = service_logic.update_order_status(order_id, status.status)
        
        if service_response is None:
            raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
        return service_response
    except HTTPException:
        raise
    except Exception as e:
        print("Error in update_order_status:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{order_id}")
async def delete_order_by_id(order_id: int, db: Session = Depends(get_db)):
    try:
        service_logic = OrdersLogic(db)

        service_response = service_logic.delete_order_by_id(order_id)
        
        if service_response is None:
            raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
        return {
            "message": f"Order {order_id} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        print("Error in delete_order_by_id:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))
    