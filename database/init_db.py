from database.db import Base, engine
import database.models

def create_database():
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully.")

if __name__ == "__main__":
    create_database()