from fastapi import FastAPI

app = FastAPI(
    title="FreshScape Market POS API",
    version="1.0.0"
)

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