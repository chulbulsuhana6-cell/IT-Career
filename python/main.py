from fastapi import FastAPI
from sqlalchemy import text
from python.database import engine

from python.routers import auth, users


app = FastAPI(
    title="IT Career Backend API",
    description="Backend API built with FastAPI, postgreSQL, SQLAlchemy, and JWT for authentication. ",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def home():
    return {"message": "My Python backend is working!"}

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }