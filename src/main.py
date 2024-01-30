from fastapi import FastAPI
from resources.auth_resource import router as auth_router
from resources.admin_resource import router as admin_router
from resources.customer_resource import router as customer_router
from resources.room_resource import router as room_router
from resources.reservation_resource import router as reservation_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(customer_router)
app.include_router(room_router)
app.include_router(reservation_router)
