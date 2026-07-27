from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.categories import router as category_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.products import router as product_router

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

app.include_router(category_router)
app.include_router(inventory_router)
app.include_router(product_router)


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