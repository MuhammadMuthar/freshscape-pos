from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.categories import router as category_router
from app.api.routes.customers import router as customer_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.products import router as product_router
from app.api.routes.purchase_orders import router as purchase_order_router
from app.api.routes.returns import router as return_router
from app.api.routes.sales import router as sale_router
from app.api.routes.suppliers import router as supplier_router

app = FastAPI(
    title="FreshScape Market POS API",
    version="1.0.0",
)

# TODO: narrow this down to the real frontend origin once it's deployed
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(customer_router)
app.include_router(inventory_router)
app.include_router(product_router)
app.include_router(purchase_order_router)
app.include_router(return_router)
app.include_router(sale_router)
app.include_router(supplier_router)


@app.get("/")
def root():
    return {
        "message": "FreshScape Market POS API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

from fastapi.staticfiles import StaticFiles

# Mount static frontend pages
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")