from fastapi import FastAPI
from routers.chat_messages import router as chat_messages_router
from routers.items import router as items_router
from routers.restaurants import router as restaurants_router
from routers.Orders import router as orders_router


app = FastAPI(title="Food Ordering API")

app.include_router(chat_messages_router)
app.include_router(items_router)
app.include_router(restaurants_router)
app.include_router(orders_router)