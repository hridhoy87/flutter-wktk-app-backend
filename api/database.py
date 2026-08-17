import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

# Neon DB Connection String from Environment
raw_url = os.getenv("DATABASE_URL")

# Compatibility fix for SQLAlchemy 1.4+ (postgres:// -> postgresql://)
if raw_url and raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql://", 1)

# Default fallback (removed for security)
DATABASE_URL = raw_url

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(
    DATABASE_URL, 
    echo=True,
    # Standard SSL config for Neon
    connect_args={"sslmode": "require"} if "postgresql" in DATABASE_URL else {}
)

def init_db():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Database Init Error: {e}")

def get_session():
    with Session(engine) as session:
        yield session
