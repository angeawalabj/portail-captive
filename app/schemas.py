from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ----------------- USERS -----------------
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: str  # "admin" ou "staff"

class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]

class UserOut(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    class Config:
        orm_mode = True

# ----------------- CLIENTS -----------------
class ClientBase(BaseModel):
    username: str

class ClientCreate(ClientBase):
    password: str
    plan_type: str  # "time", "data", "unlimited"
    quota_seconds: Optional[int] = None
    quota_bytes: Optional[int] = None
    expires_at: Optional[datetime] = None

class ClientUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    plan_type: Optional[str]
    quota_seconds: Optional[int]
    quota_bytes: Optional[int]
    expires_at: Optional[datetime]
    is_active: Optional[bool]

class ClientOut(ClientBase):
    id: int
    plan_type: str
    quota_seconds: Optional[int]
    quota_bytes: Optional[int]
    expires_at: Optional[datetime]
    is_active: bool
    created_at: datetime
    class Config:
        orm_mode = True

# ----------------- SESSIONS -----------------
class SessionBase(BaseModel):
    client_id: int

class SessionCreate(SessionBase):
    mac: Optional[str] = None
    ip: Optional[str] = None

class SessionUpdate(BaseModel):
    end_at: Optional[datetime]
    bytes_up: Optional[int]
    bytes_down: Optional[int]

class SessionOut(SessionBase):
    id: int
    mac: Optional[str]
    ip: Optional[str]
    start_at: datetime
    end_at: Optional[datetime]
    bytes_up: int
    bytes_down: int
    class Config:
        orm_mode = True
