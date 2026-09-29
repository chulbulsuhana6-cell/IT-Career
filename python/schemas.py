from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr

class UserResponse(BaseModel):
        id: int
        name: str
        email: EmailStr

class JobCreate(BaseModel):
    company: str = Field(min_length=2, max_length=150)
    role: str = Field(min_length=2, max_length=150)
    location: str = Field(min_length=2, max_length=150)
    status: str = Field(default="Applied", min_length=2, max_length=50)


class JobResponse(BaseModel):
    id: int
    company: str
    role: str
    location: str
    status: str       