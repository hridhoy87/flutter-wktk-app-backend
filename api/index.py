from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import Response, FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from sqlmodel import Session, select, text
from datetime import datetime, timedelta
from typing import List, Optional
import hashlib
import time
import os

from .database import get_session, init_db, engine
from .models import User, UserCreate, UserRead, Token, TokenData, Channel, LoginRequest, UserUpdate, ChannelRead, ChannelPasswordUpdate, ChannelVerify, ChannelCreate, UserAdminUpdate, ChannelAdminUpdate
from .admin_dashboard import ADMIN_DASHBOARD_HTML
from .auth import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

app = FastAPI(title="WalkieTalkie Backend")

class VercelQueryPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path_param = request.query_params.get("path")
        if path_param and request.url.path in ("/api/index", "/api", "/"):
            request.scope["path"] = "/" + path_param.lstrip("/")
        return await call_next(request)

app.add_middleware(VercelQueryPathMiddleware)

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
    # Initialize tables
    init_db()
    
    # Safety cleanup for any temporary channels abandoned more than 12h ago
    with Session(engine) as session:
        threshold = datetime.utcnow() - timedelta(hours=12)
        stale = session.exec(select(Channel).where(
            Channel.is_temporary == True,
            Channel.created_at < threshold
        )).all()
        for ch in stale:
            session.delete(ch)
        session.commit()

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
@app.get("/api")
@app.get("/api/index")
def health_check():
    return {"status": "online", "message": "WalkieTalkie API is running", "version": "1.1"}

@app.get("/time")
@app.get("/api/time")
@app.get("/api/index/time")
def get_server_time():
    """
    High-precision server timestamp in UTC milliseconds.
    Used by client devices for network time synchronization and PTT floor arbitration.
    """
    now = time.time()
    return {
        "server_time_ms": int(now * 1000),
        "timestamp_iso": datetime.utcnow().isoformat() + "Z"
    }

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
        normalized_phone = "".join([c for c in login_data.phone if c.isdigit()])
        user = session.exec(select(User).where((User.phone == normalized_phone) | (User.phone == login_data.phone))).first()
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

def is_user_entitled_to_channel(channel: Channel, user: User) -> bool:
    if user.is_admin:
        return True
    if channel.admin_id == user.id:
        return True
    if channel.allowed_user_ids:
        allowed = [uid.strip() for uid in channel.allowed_user_ids.split(",") if uid.strip()]
        return str(user.id) in allowed or user.phone in allowed
    # When allowed_user_ids is None/empty:
    # Protected or temporary channels require explicit membership or admin
    if channel.is_protected or channel.is_temporary:
        return False
    # Only completely open Global channel allows all users when allowed_user_ids is not set
    if channel.name and channel.name.lower() == "global":
        return True
    return False

# --- Channels ---

@app.get("/channels/public", response_model=List[ChannelRead])
def get_public_channels(session: Session = Depends(get_session)):
    """
    Public endpoint for registration dropdown to display available subscription channels.
    Returns non-temporary channels.
    """
    channels = session.exec(select(Channel).where(Channel.is_temporary == False)).all()
    if not channels:
        seed_channels()
        channels = session.exec(select(Channel).where(Channel.is_temporary == False)).all()
    return channels

@app.get("/channels", response_model=List[ChannelRead])
def get_channels(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    all_channels = session.exec(select(Channel)).all()

    # LAZY INITIALIZATION: Automatically seed the default channels if the database is empty
    if not all_channels:
        seed_channels()
        all_channels = session.exec(select(Channel)).all()

    # Update activity for temporary channels being viewed
    for c in all_channels:
        if c.is_temporary:
            c.created_at = datetime.utcnow()
            session.add(c)
    session.commit()

    if current_user.is_admin:
        return all_channels

    return [c for c in all_channels if is_user_entitled_to_channel(c, current_user)]

@app.get("/channels/{channel_id}/users", response_model=List[UserRead])
def get_channel_users(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    channel = session.get(Channel, channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    all_approved = session.exec(select(User).where(User.is_approved == True)).all()
    if current_user.is_admin:
        return all_approved

    if not is_user_entitled_to_channel(channel, current_user):
        raise HTTPException(status_code=403, detail="Not entitled to view this channel")

    if channel.allowed_user_ids:
        allowed = [uid.strip() for uid in channel.allowed_user_ids.split(",") if uid.strip()]
        peer_ids = set(allowed)
        if channel.admin_id:
            peer_ids.add(str(channel.admin_id))
        return [u for u in all_approved if str(u.id) in peer_ids or u.phone in peer_ids]
    else:
        return all_approved

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

@app.delete("/channels/{channel_id}")
def delete_channel(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    channel = session.get(Channel, channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    if not channel.is_temporary:
        raise HTTPException(status_code=400, detail="Cannot delete permanent channels")

    if channel.admin_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this channel")

    session.delete(channel)
    session.commit()
    return {"status": "success", "message": "Channel deleted"}

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
    all_approved = session.exec(select(User).where(User.is_approved == True)).all()
    if current_user.is_admin:
        return all_approved

    # Regular user: Collect all members across all channels this user is entitled to
    all_channels = session.exec(select(Channel)).all()
    my_channels = [c for c in all_channels if is_user_entitled_to_channel(c, current_user)]

    # Collect all peer user IDs / phones across the user's entitled channels
    entitled_peer_ids = {str(current_user.id), current_user.phone}
    has_unrestricted_global = False

    for c in my_channels:
        if c.admin_id:
            entitled_peer_ids.add(str(c.admin_id))
        if c.allowed_user_ids:
            for uid in c.allowed_user_ids.split(","):
                if uid.strip():
                    entitled_peer_ids.add(uid.strip())
        elif c.name and c.name.lower() == "global" and not c.is_protected:
            has_unrestricted_global = True

    if has_unrestricted_global:
        return all_approved

    filtered_users = [
        u for u in all_approved
        if str(u.id) in entitled_peer_ids or u.phone in entitled_peer_ids
    ]
    return filtered_users

@app.post("/register", response_model=UserRead)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    try:
        # Normalize phone number (keep only digits)
        normalized_phone = "".join([c for c in user_in.phone if c.isdigit()])

        if not normalized_phone:
             raise HTTPException(status_code=400, detail="Invalid phone number")

        db_user = session.exec(select(User).where((User.phone == normalized_phone) | (User.phone == user_in.phone))).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Phone already registered")

        hashed_pw = get_password_hash(user_in.password)
        new_user = User(
            phone=normalized_phone,
            legal_name=user_in.legal_name,
            password_hash=hashed_pw,
            is_approved=False,
            is_admin=False
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # If user requested to subscribe to specific channels, add user to allowed_user_ids
        if user_in.channel_ids:
            for ch_id in user_in.channel_ids:
                ch = session.get(Channel, ch_id)
                if ch:
                    existing = [uid.strip() for uid in ch.allowed_user_ids.split(",") if uid.strip()] if ch.allowed_user_ids else []
                    if str(new_user.id) not in existing and normalized_phone not in existing:
                        existing.append(str(new_user.id))
                        ch.allowed_user_ids = ",".join(existing)
                        session.add(ch)
            session.commit()

        return new_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Super Admin Dashboard & APIs ---

@app.get("/api/super-admin", response_class=HTMLResponse)
@app.get("/super-admin", response_class=HTMLResponse)
def serve_super_admin_dashboard():
    """
    Serves the modern, high-performance Super Admin Dashboard console.
    """
    return HTMLResponse(content=ADMIN_DASHBOARD_HTML)

@app.get("/api/super-admimn", include_in_schema=False)
@app.get("/super-admimn", include_in_schema=False)
def redirect_typo_admin():
    """
    Redirects old typo URL to /api/super-admin.
    """
    return RedirectResponse(url="/api/super-admin")

@app.get("/admin/stats")
def get_admin_stats(admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    all_users = session.exec(select(User)).all()
    all_channels = session.exec(select(Channel)).all()
    return {
        "total_users": len(all_users),
        "approved_users": len([u for u in all_users if u.is_approved]),
        "pending_users": len([u for u in all_users if not u.is_approved]),
        "admin_users": len([u for u in all_users if u.is_admin]),
        "total_channels": len(all_channels),
        "protected_channels": len([c for c in all_channels if c.is_protected]),
        "public_channels": len([c for c in all_channels if not c.is_protected and not c.is_temporary]),
        "temporary_channels": len([c for c in all_channels if c.is_temporary]),
    }

@app.get("/admin/users", response_model=List[UserRead])
def get_all_users_admin(admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    return session.exec(select(User).order_by(User.id)).all()

@app.post("/admin/users", response_model=UserRead)
def create_user_admin(user_in: UserCreate, admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    normalized_phone = "".join([c for c in user_in.phone if c.isdigit()]) or user_in.phone
    existing = session.exec(select(User).where((User.phone == normalized_phone) | (User.phone == user_in.phone))).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    new_user = User(
        phone=normalized_phone,
        legal_name=user_in.legal_name,
        password_hash=get_password_hash(user_in.password),
        is_approved=user_in.is_approved,
        is_admin=user_in.is_admin
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    if user_in.channel_ids:
        for ch_id in user_in.channel_ids:
            ch = session.get(Channel, ch_id)
            if ch:
                allowed = [uid.strip() for uid in ch.allowed_user_ids.split(",") if uid.strip()] if ch.allowed_user_ids else []
                if str(new_user.id) not in allowed:
                    allowed.append(str(new_user.id))
                    ch.allowed_user_ids = ",".join(allowed)
                    session.add(ch)
        session.commit()
    return new_user

@app.patch("/admin/users/{user_id}", response_model=UserRead)
def update_user_admin(user_id: int, user_update: UserAdminUpdate, admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    target = session.get(User, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.legal_name is not None:
        target.legal_name = user_update.legal_name
    if user_update.phone is not None:
        normalized = "".join([c for c in user_update.phone if c.isdigit()]) or user_update.phone
        target.phone = normalized
    if user_update.password is not None and user_update.password.strip():
        target.password_hash = get_password_hash(user_update.password.strip())
    if user_update.is_approved is not None:
        target.is_approved = user_update.is_approved
    if user_update.is_admin is not None:
        target.is_admin = user_update.is_admin
    session.add(target)
    session.commit()

    if user_update.channel_ids is not None:
        all_channels = session.exec(select(Channel)).all()
        for ch in all_channels:
            allowed = [uid.strip() for uid in ch.allowed_user_ids.split(",") if uid.strip()] if ch.allowed_user_ids else []
            should_have = ch.id in user_update.channel_ids
            has = str(target.id) in allowed or target.phone in allowed
            if should_have and not has:
                allowed.append(str(target.id))
                ch.allowed_user_ids = ",".join(allowed)
                session.add(ch)
            elif not should_have and has:
                allowed = [x for x in allowed if x != str(target.id) and x != target.phone]
                ch.allowed_user_ids = ",".join(allowed) if allowed else None
                session.add(ch)
        session.commit()
    session.refresh(target)
    return target

@app.delete("/admin/users/{user_id}")
def delete_user_admin(user_id: int, admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    target = session.get(User, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    if target.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own active admin account")
    
    all_channels = session.exec(select(Channel)).all()
    for ch in all_channels:
        if ch.allowed_user_ids:
            allowed = [uid.strip() for uid in ch.allowed_user_ids.split(",") if uid.strip()]
            if str(target.id) in allowed or target.phone in allowed:
                allowed = [x for x in allowed if x != str(target.id) and x != target.phone]
                ch.allowed_user_ids = ",".join(allowed) if allowed else None
                session.add(ch)
        if ch.admin_id == target.id:
            ch.admin_id = None
            session.add(ch)
    session.delete(target)
    session.commit()
    return {"status": "success", "message": "User deleted"}

@app.get("/admin/channels", response_model=List[ChannelRead])
def get_all_channels_admin(admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    return session.exec(select(Channel).order_by(Channel.id)).all()

@app.post("/admin/channels", response_model=ChannelRead)
def create_channel_admin(ch_in: ChannelCreate, admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    new_ch = Channel(
        name=ch_in.name,
        is_protected=ch_in.is_protected,
        is_temporary=ch_in.is_temporary,
        admin_id=ch_in.admin_id if hasattr(ch_in, 'admin_id') and ch_in.admin_id is not None else admin.id,
        allowed_user_ids=ch_in.allowed_user_ids,
        password_hash=get_password_hash(ch_in.password) if ch_in.password else None
    )
    session.add(new_ch)
    session.commit()
    session.refresh(new_ch)
    return new_ch

@app.patch("/admin/channels/{channel_id}", response_model=ChannelRead)
def update_channel_admin(channel_id: int, ch_update: ChannelAdminUpdate, admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    ch = session.get(Channel, channel_id)
    if not ch:
        raise HTTPException(status_code=404, detail="Channel not found")
    if ch_update.name is not None:
        ch.name = ch_update.name
    if ch_update.is_protected is not None:
        ch.is_protected = ch_update.is_protected
    if ch_update.password is not None and ch_update.password.strip():
        ch.password_hash = get_password_hash(ch_update.password.strip())
    if ch_update.is_temporary is not None:
        ch.is_temporary = ch_update.is_temporary
    if ch_update.admin_id is not None:
        ch.admin_id = ch_update.admin_id if ch_update.admin_id > 0 else None
    if ch_update.allowed_user_ids is not None:
        ch.allowed_user_ids = ch_update.allowed_user_ids if ch_update.allowed_user_ids.strip() else None
    session.add(ch)
    session.commit()
    session.refresh(ch)
    return ch

@app.delete("/admin/channels/{channel_id}")
def delete_channel_admin(channel_id: int, admin: User = Depends(get_current_admin), session: Session = Depends(get_session)):
    ch = session.get(Channel, channel_id)
    if not ch:
        raise HTTPException(status_code=404, detail="Channel not found")
    session.delete(ch)
    session.commit()
    return {"status": "success", "message": "Channel deleted"}

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