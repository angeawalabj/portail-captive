from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import crud, schemas
from app.models import Base

# ==========================
# Setup DB test en mémoire
# ==========================
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(override_get_db())

# ==========================
# Tests USERS
# ==========================
def test_create_and_get_user():
    user_in = schemas.UserCreate(username="alice", password="secret", role="admin")
    user = crud.create_user(db, user_in)
    
    assert user.username == "alice"
    assert crud.verify_password("secret", user.password_hash)
    
    fetched = crud.get_user(db, user.id)
    assert fetched.username == "alice"

def test_update_and_delete_user():
    user_in = schemas.UserCreate(username="bob", password="pass123", role="staff")
    user = crud.create_user(db, user_in)
    
    update_data = schemas.UserUpdate(username="bob_updated", is_active=False)
    updated = crud.update_user(db, user.id, update_data)
    
    assert updated.username == "bob_updated"
    assert updated.is_active is False
    
    crud.delete_user(db, user.id)
    assert crud.get_user(db, user.id) is None

# ==========================
# Tests CLIENTS
# ==========================
def test_create_and_get_client():
    client_in = schemas.ClientCreate(username="client1", password="clientpass", plan_type="time")
    client = crud.create_client(db, client_in)
    
    assert client.username == "client1"
    assert crud.verify_password("clientpass", client.password_hash)
    
    fetched = crud.get_client(db, client.id)
    assert fetched.username == "client1"

def test_update_and_delete_client():
    client_in = schemas.ClientCreate(username="client2", password="pass2", plan_type="data")
    client = crud.create_client(db, client_in)
    
    update_data = schemas.ClientUpdate(username="client2_updated", is_active=False)
    updated = crud.update_client(db, client.id, update_data)
    
    assert updated.username == "client2_updated"
    assert updated.is_active is False
    
    crud.delete_client(db, client.id)
    assert crud.get_client(db, client.id) is None

# ==========================
# Tests SESSIONS
# ==========================
def test_create_and_update_session():
    client_in = schemas.ClientCreate(username="sess_client", password="pass", plan_type="time")
    client = crud.create_client(db, client_in)
    
    session_in = schemas.SessionCreate(client_id=client.id, mac="AA:BB:CC:DD:EE:FF", ip="192.168.1.2")
    session = crud.create_session(db, session_in)
    
    assert session.mac == "AA:BB:CC:DD:EE:FF"
    assert session.client_id == client.id
    
    update_data = schemas.SessionUpdate(bytes_up=1024, bytes_down=2048, end_at=datetime.utcnow())
    updated = crud.update_session(db, session.id, update_data)
    
    assert updated.bytes_up == 1024
    assert updated.bytes_down == 2048
    assert updated.end_at is not None
    
    crud.delete_session(db, session.id)
    assert crud.get_sessions(db, 0, 100) == []
