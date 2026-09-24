from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from python.auth import create_access_token
from python.database import engine
from python.dependencies import get_current_user

from python.models import User
from python.schemas import UserCreate, UserLogin
from python.security import hash_password, verify_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/login")
def login_user( user_data:UserLogin):
    with Session(engine) as session:
        user = session.query(User).filter(User.email == user_data.email).first()

        if  user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )
        if not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(data={"sub": user.email})

        return {"access_token": access_token, "token_type": "bearer"}

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


@router.get("/")
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


@router.get("/{user_id}")
def get_user(user_id: int):
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


@router.put("/{user_id}")
def update_user(user_id: int, user_data: UserCreate):
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
def delete_user(user_id: int):
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