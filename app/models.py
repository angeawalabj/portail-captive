from sqlalchemy import Column, Integer, String, Boolean, Enum, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import enum
from datetime import datetime

Base = declarative_base()

# =========================
# ENUMS
# =========================
class UserRole(enum.Enum):
    admin = "admin"
    staff = "staff"

class PlanType(enum.Enum):
    time = "time"
    data = "data"
    unlimited = "unlimited"

# =========================
# USERS (admin/staff)
# =========================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

# =========================
# CLIENTS
# =========================
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    plan_type = Column(Enum(PlanType), nullable=False)
    quota_seconds = Column(Integer, nullable=True)
    quota_bytes = Column(BigInteger, nullable=True)
    expires_at = Column(TIMESTAMP, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    sessions = relationship("Session", back_populates="client", cascade="all, delete-orphan")

# =========================
# SESSIONS
# =========================
class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    mac = Column(String, nullable=True)
    ip = Column(String, nullable=True)
    start_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    end_at = Column(TIMESTAMP, nullable=True)
    bytes_up = Column(BigInteger, default=0)
    bytes_down = Column(BigInteger, default=0)

    client = relationship("Client", back_populates="sessions")
