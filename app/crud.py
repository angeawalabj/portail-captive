from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------- USERS -----------------
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=hashed_password,
        role=user.role,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    user = get_user(db, user_id)
    if not user:
        return None
    if user_update.username:
        user.username = user_update.username
    if user_update.password:
        user.password_hash = pwd_context.hash(user_update.password)
    if user_update.role:
        user.role = user_update.role
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ----------------- CLIENTS -----------------
def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def get_client_by_username(db: Session, username: str):
    return db.query(models.Client).filter(models.Client.username == username).first()

def create_client(db: Session, client: schemas.ClientCreate):
    hashed_password = pwd_context.hash(client.password)
    db_client = models.Client(
        username=client.username,
        password_hash=hashed_password,
        plan_type=client.plan_type,
        quota_seconds=client.quota_seconds,
        quota_bytes=client.quota_bytes,
        expires_at=client.expires_at,
        is_active=True
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: int, client_update: schemas.ClientUpdate):
    client = get_client(db, client_id)
    if not client:
        return None
    if client_update.username:
        client.username = client_update.username
    if client_update.password:
        client.password_hash = pwd_context.hash(client_update.password)
    if client_update.plan_type:
        client.plan_type = client_update.plan_type
    if client_update.quota_seconds is not None:
        client.quota_seconds = client_update.quota_seconds
    if client_update.quota_bytes is not None:
        client.quota_bytes = client_update.quota_bytes
    if client_update.expires_at is not None:
        client.expires_at = client_update.expires_at
    if client_update.is_active is not None:
        client.is_active = client_update.is_active
    db.commit()
    db.refresh(client)
    return client

def delete_client(db: Session, client_id: int):
    client = get_client(db, client_id)
    if client:
        db.delete(client)
        db.commit()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()

# ----------------- SESSIONS -----------------
def get_sessions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Session).offset(skip).limit(limit).all()

def create_session(db: Session, session: schemas.SessionCreate):
    db_session = models.Session(
        client_id=session.client_id,
        mac=session.mac,
        ip=session.ip,
        start_at=datetime.utcnow(),
        bytes_up=0,
        bytes_down=0
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def update_session(db: Session, session_id: int, session_update: schemas.SessionUpdate):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        return None
    if session_update.end_at:
        session.end_at = session_update.end_at
    if session_update.bytes_up is not None:
        session.bytes_up = session_update.bytes_up
    if session_update.bytes_down is not None:
        session.bytes_down = session_update.bytes_down
    db.commit()
    db.refresh(session)
    return session

def delete_session(db: Session, session_id: int):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
