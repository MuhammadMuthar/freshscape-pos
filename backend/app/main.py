from fastapi import FastAPI

from app.api.routes.categories import router as category_router

app = FastAPI(
    title="FreshScape Market POS API",
    version="1.0.0",
)

app.include_router(category_router)


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