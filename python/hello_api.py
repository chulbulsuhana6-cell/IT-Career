from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from python.database import engine
from python.models import User


app = FastAPI()


class UserCreate(BaseModel):
    name: str
    email: str


@app.get("/")
def home():
    return {"message": "My Python backend is working!"}


@app.post("/users")
def create_user(user: UserCreate):
    with Session(engine) as session:
        new_user = User(
            name=user.name,
            email=user.email
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }


@app.get("/users")
def get_users():
    with Session(engine) as session:
        users = session.query(User).all()

        return [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            for user in users
        ]