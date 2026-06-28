from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class UserBase(SQLModel):
    phone: str = Field(index=True, unique=True)
    legal_name: str
    is_approved: bool = Field(default=False)
    is_admin: bool = Field(default=False)

class User(UserBase, table=True):
    __tablename__ = "app_user"
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

class ChannelBase(SQLModel):
    name: str
    is_protected: bool = Field(default=False)
    is_temporary: bool = Field(default=False)
    allowed_user_ids: Optional[str] = Field(default=None)

class Channel(ChannelBase, table=True):
    __tablename__ = "app_channel"
    id: Optional[int] = Field(default=None, primary_key=True)
    admin_id: Optional[int] = Field(default=None, foreign_key="app_user.id")
    password_hash: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    admin: Optional[User] = Relationship()

class ChannelCreate(ChannelBase):
    password: Optional[str] = None

class ChannelRead(ChannelBase):
    id: int
    admin_id: Optional[int]

class ChannelPasswordUpdate(SQLModel):
    password: str

class ChannelVerify(SQLModel):
    channel_id: int
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    phone: Optional[str] = None

class LoginRequest(SQLModel):
    phone: str
    password: str

class UserUpdate(SQLModel):
    legal_name: Optional[str] = None
    password: Optional[str] = None
