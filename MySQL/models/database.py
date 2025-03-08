from sqlalchemy.orm import Session
from config.db_config import engine
from models.laptop import Base

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Get database session
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
