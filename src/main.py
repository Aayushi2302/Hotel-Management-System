from fastapi import FastAPI


from resources.auth_resource import router as auth_router
from resources.admin_resource import router as admin_router
from resources.customer_resource import router as customer_router
from resources.room_resource import router as room_router
from resources.reservation_resource import router as reservation_router

tags_metadata = [
    {
        "name": "authentication",
        "description": "Operations related with user authentication.",
    },
    {
        "name": "employee",
        "description": "Operations on employees.",
    },
    {
        "name": "customer",
        "description": "Operations on customers.",
    },
    {
        "name": "reservation",
        "description": "Operations related to room reservation.",
    },
    {
        "name": "room",
        "description": "Operations related to room.",
    },
]

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/openapi.json",
    openapi_tags=tags_metadata
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(customer_router)
app.include_router(room_router)
app.include_router(reservation_router)
