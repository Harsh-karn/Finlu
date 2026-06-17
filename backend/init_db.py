from app.database import engine, Base
import app.models # Ensures all models are registered with Base.metadata

print("Creating database tables if they do not exist...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
