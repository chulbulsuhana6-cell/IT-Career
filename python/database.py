import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from python.models import Base


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from .env")

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    connection.execute(
        text(
            "ALTER TABLE users "
            "ADD COLUMN IF NOT EXISTS hashed_password VARCHAR(255)"
        )
    )
    connection.commit()

Base.metadata.create_all(engine)

print("Database updated successfully!")