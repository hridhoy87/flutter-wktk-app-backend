import os
import hashlib
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # In production, this will raise an error if not set, preventing insecure defaults
    if os.getenv("VERCEL") or os.getenv("PRODUCTION"):
        raise RuntimeError("SECRET_KEY environment variable is not set!")
    SECRET_KEY = "dev-secret-key-change-me-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 Days

def get_password_hash(password: str) -> str:
    # Pre-hash with SHA-256 to support unlimited length
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    # Generate bcrypt hash from the SHA-256 result
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(sha256_hash.encode(), salt)
    return hashed.decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Pre-hash incoming password with SHA-256
        sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        # Compare with the stored bcrypt hash
        return bcrypt.checkpw(sha256_hash.encode(), hashed_password.encode())
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
