from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import Response, FileResponse
from sqlmodel import Session, select, text
from typing import List
import hashlib
import time
import os

from .database import get_session, init_db, engine
from .models import User, UserCreate, UserRead, Token, TokenData, Channel, LoginRequest, UserUpdate, ChannelRead, ChannelPasswordUpdate, ChannelVerify, ChannelCreate
from .auth import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

app = FastAPI(title="WalkieTalkie Backend")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.on_event("startup")
def on_startup():
    # Only initialize tables here. This is very fast and prevents login/register errors.
    # We defer the slower seed_channels() to lazy initialization below.
    init_db()

def seed_channels():
    with Session(engine) as session:
        # We use fixed IDs 1-7 for seeded channels to ensure frontend predictability.
        # Global = 1, Group 1 = 2, ..., Group 6 = 7.
        has_changes = False
        
        # Check Global
        if not session.get(Channel, 1):
            session.add(Channel(id=1, name="Global", is_protected=False))
            has_changes = True

        # Check for 6 groups
        for i in range(1, 7):
            target_id = i + 1
            if not session.get(Channel, target_id):
                session.add(Channel(id=target_id, name=f"Group {i}", is_protected=True))
                has_changes = True
        
        if has_changes:
            session.commit()
            # Reset sequence for Postgres to avoid ID collision on next manual creation
            try:
                session.exec(text("SELECT setval('app_channel_id_seq', (SELECT MAX(id) FROM app_channel))"))
                session.commit()
            except Exception as e:
                # Fallback for non-postgres or if sequence name is different
                print(f"Database sequence sync skipped or failed: {e}")

# --- Helpers & Dependencies ---

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception
        token_data = TokenData(phone=phone)
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.phone == token_data.phone)).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not an admin")
    return current_user

# --- Routes ---

@app.get("/")
def health_check():
    return {"status": "online", "message": "WalkieTalkie API is running", "version": "1.1"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Serves the physical favicon.ico file from the api/static/ directory.
    Includes a fallback to 204 No Content just in case the file isn't bundled by Vercel.
    """
    # Dynamically locate the api/ directory where index.py lives
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Target the api/static/favicon.ico file
    favicon_path = os.path.join(base_dir, "static", "favicon.ico")

    # Serve the file if it exists, otherwise fallback safely
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    return Response(status_code=204)

@app.post("/login", response_model=Token)
def login(login_data: LoginRequest, session: Session = Depends(get_session)):
    """
    Login using JSON data.
    Body: {"phone": "...", "password": "..."}
    """
    try:
        user = session.exec(select(User).where(User.phone == login_data.phone)).first()
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect phone or password")
        if not user.is_approved:
            raise HTTPException(status_code=403, detail="User not approved by admin")

        access_token = create_access_token(data={"sub": user.phone})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/home", response_model=UserRead)
def get_home_data(current_user: User = Depends(get_current_user)):
    """
    Protected route. Returns the current user's profile and state.
    """
    return current_user

# --- Channels ---

@app.get("/channels", response_model=List[ChannelRead])
def get_channels(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    all_channels = session.exec(select(Channel)).all()

    # LAZY INITIALIZATION: Automatically seed the default channels if the database is empty
    if not all_channels:
        seed_channels()
        all_channels = session.exec(select(Channel)).all()

    filtered = []
    for c in all_channels:
        if not c.is_temporary:
            filtered.append(c)
        else:
            if c.allowed_user_ids:
                allowed = c.allowed_user_ids.split(",")
                if str(current_user.id) in allowed or c.admin_id == current_user.id:
                    filtered.append(c)
            elif c.admin_id == current_user.id:
                filtered.append(c)
    return filtered

@app.post("/channels/temp", response_model=ChannelRead)
def create_temp_channel(
        channel_in: ChannelCreate,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    # Ensure admin is in allowed_user_ids if not already
    allowed = channel_in.allowed_user_ids or ""
    if str(current_user.id) not in allowed.split(","):
        allowed = f"{allowed},{current_user.id}" if allowed else str(current_user.id)

    new_channel = Channel(
        name=channel_in.name,
        is_protected=channel_in.is_protected,
        is_temporary=True,
        allowed_user_ids=allowed,
        admin_id=current_user.id,
        password_hash=get_password_hash(channel_in.password) if channel_in.password else None
    )
    session.add(new_channel)
    session.commit()
    session.refresh(new_channel)
    return new_channel

@app.post("/channels/verify")
def verify_channel_password(
        data: ChannelVerify,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    channel = session.get(Channel, data.channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    if not channel.is_protected:
        return {"status": "success"}
    if not channel.password_hash:
        raise HTTPException(status_code=400, detail="Channel password not set by admin yet")
    if not verify_password(data.password, channel.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect channel password")
    return {"status": "success"}

@app.patch("/channels/{channel_id}/password")
def update_channel_password(
        channel_id: int,
        data: ChannelPasswordUpdate,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    channel = session.get(Channel, channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    # Prevent hijacking of public/system channels
    # If admin_id is None, it's a system channel - only global admins can modify it
    if channel.admin_id is None:
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="System channels can only be modified by global admins")
    elif channel.admin_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not the channel admin")

    channel.password_hash = get_password_hash(data.password)
    # If it was a system channel and an admin is setting a password, 
    # they become the specific admin for this channel's settings
    if channel.admin_id is None:
        channel.admin_id = current_user.id

    session.add(channel)
    session.commit()
    return {"status": "success", "message": "Channel password updated"}

@app.patch("/users/me", response_model=UserRead)
def update_user_me(
        user_update: UserUpdate,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    if user_update.legal_name is not None:
        current_user.legal_name = user_update.legal_name
    if user_update.password is not None:
        current_user.password_hash = get_password_hash(user_update.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@app.get("/users/online", response_model=List[UserRead])
def get_online_users(
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    users = session.exec(select(User).where(User.is_approved == True)).all()
    return users

@app.post("/register", response_model=UserRead)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    try:
        db_user = session.exec(select(User).where(User.phone == user_in.phone)).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Phone already registered")

        hashed_pw = get_password_hash(user_in.password)
        new_user = User(
            phone=user_in.phone,
            legal_name=user_in.legal_name,
            password_hash=hashed_pw,
            is_approved=False,
            is_admin=False
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Admin Routes ---

@app.get("/admin/pending-users", response_model=List[UserRead])
def get_pending_users(admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    users = session.exec(select(User).where(User.is_approved == False)).all()
    return users

@app.patch("/admin/approve-user/{user_id}")
def approve_user(user_id: int, admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_approved = True
    session.add(user)
    session.commit()
    return {"status": "success"}

@app.delete("/admin/reject-user/{user_id}")
def reject_user(user_id: int, admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"status": "deleted"}

# --- Utility Routes ---

@app.get("/turn-credentials")
def get_turn_credentials(current_user: User = Depends(get_current_user)):
    secret = os.getenv("COTURN_SECRET")
    if not secret:
        # Fallback for dev, but in production this should be set
        secret = "dev-coturn-secret"

    ttl = 3600 * 24
    timestamp = int(time.time()) + ttl
    username = f"{timestamp}:{current_user.phone}"
    password = hashlib.sha1(f"{username}:{secret}".encode()).hexdigest()

    return {
        "username": username,
        "password": password,
        "ttl": ttl,
        "uris": [
            "stun:stun1.l.google.com:19302",
            "stun:stun2.l.google.com:19302",
        ]
    }