from fastapi import FastAPI

from python.routers import auth, users


app = FastAPI()


app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def home():
    return {"message": "My Python backend is working!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}