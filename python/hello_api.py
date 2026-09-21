from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "My Python backend is working!"}