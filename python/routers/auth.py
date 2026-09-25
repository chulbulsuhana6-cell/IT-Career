from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from python.auth import create_access_token
from python.database import engine
from python.models import User
from python.schemas import UserLogin
from python.security import verify_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login_user(user_data: UserLogin):
    with Session(engine) as session:
        user = session.query(User).filter(
            User.email == user_data.email
        ).first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not verify_password(
            user_data.password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            {"sub": user.email}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }