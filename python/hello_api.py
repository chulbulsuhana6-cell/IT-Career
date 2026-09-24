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


@app.get("/users/{user_id}")
def get_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)

        if user is None:
            return {"message": "User not found"}

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)

        if user is None:
            return {"message": "User not found"}

        session.delete(user)
        session.commit()

        return {"message": "User deleted successfully"}


@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: UserCreate):
    with Session(engine) as session:
        user = session.get(User, user_id)

        if user is None:
            return {"message": "User not found"}

        user.name = user_data.name
        user.email = user_data.email

        session.commit()
        session.refresh(user)

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }