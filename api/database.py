import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

# Neon DB Connection String from Environment
raw_url = os.getenv("DATABASE_URL")

# Compatibility fix for SQLAlchemy 1.4+ (postgres:// -> postgresql://)
if raw_url and raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql://", 1)

# Default fallback (from your previous read)
DATABASE_URL = raw_url or 'postgresql://neondb_owner:npg_pWiU4JO3NsFS@ep-nameless-forest-aosdmrbj-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'

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
