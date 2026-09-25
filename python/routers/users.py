from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from python.database import engine
from python.dependencies import get_current_user
from python.models import User
from python.schemas import UserCreate, UserUpdate, UserResponse
from python.security import hash_password


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    with Session(engine) as session:
        new_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hash_password(user.password)
        )

        session.add(new_user)

        try:
            session.commit()
            session.refresh(new_user)
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

        return {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }


@router.get("/", response_model=list[UserResponse])
def get_users(current_user: str = Depends(get_current_user)):
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


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: str = Depends(get_current_user)
):
    with Session(engine) as session:
        user = session.get(User, user_id)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: str = Depends(get_current_user)
):
    with Session(engine) as session:
        user = session.get(User, user_id)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        user.name = user_data.name
        user.email = user_data.email

        try:
            session.commit()
            session.refresh(user)
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: str = Depends(get_current_user)
):
    with Session(engine) as session:
        user = session.get(User, user_id)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        session.delete(user)
        session.commit()

        return {
            "message": "User deleted successfully"
        }