from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(150))
    role: Mapped[str] = mapped_column(String(150))   
    location: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(String(50), default="Applied")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    