import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables
load_dotenv()

# Database connection URL
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Create engine
engine = create_engine(DATABASE_URL)

# ORM session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Metadata and Base
Base = declarative_base()
metadata = MetaData()

