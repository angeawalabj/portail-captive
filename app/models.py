from sqlalchemy import Column, Integer, String, Boolean, Enum, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import enum


Base = declarative_base()


class UserRole(enum.Enum):
    admin = "admin"
    staff = "staff"


class PlanType(enum.Enum):
    time = "time"
    data = "data"
    unlimited = "unlimited"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    plan_type = Column(Enum(PlanType), nullable=False)
    quota_seconds = Column(Integer)
    quota_bytes = Column(BigInteger)
    expires_at = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True, nullable=False)


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    mac = Column(String)
    ip = Column(String)
    start_at = Column(TIMESTAMP)
    end_at = Column(TIMESTAMP)
    bytes_up = Column(BigInteger, default=0)
    bytes_down = Column(BigInteger, default=0)


client = relationship("Client")