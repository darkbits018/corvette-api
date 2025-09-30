import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("No DATABASE_URL found in environment variables. Please create a .env file.")

# Create the SQLAlchemy engine for PostgreSQL
# The connect_args for 'check_same_thread' is specific to SQLite and not needed for PostgreSQL.
engine = create_engine(
     SQLALCHEMY_DATABASE_URL,
     pool_recycle=1800,  # Recycle connections every 30 minutes
     pool_pre_ping=True  # Optional but recommended: check connection validity before use
 )


# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
