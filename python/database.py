from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg://postgres:suhana2005@localhost:5432/it_career"

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print("Database connection successful!")
    print("Result:", result.scalar())