from sqlalchemy import text

from app.database.session import engine

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("✅ Successfully connected to MySQL!")

except Exception as e:
    print("❌ Database connection failed!")
    print(e)