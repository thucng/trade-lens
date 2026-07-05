from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import countries, dashboard

app = FastAPI(title="TradeLens")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "TradeLens"}


app.include_router(countries.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
