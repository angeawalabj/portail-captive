import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import auth, models, deps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# ==========================
# Setup DB test
# ==========================
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # DB en mémoire pour tests
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer les tables
Base.metadata.create_all(bind=engine)

# Dépendance override pour FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[deps.get_db] = override_get_db

client = TestClient(app)

# ==========================
# Tests fonctions hash
# ==========================
def test_password_hash_and_verify():
    password = "mysecretpassword"
    hashed = auth.get_password_hash(password)
    assert hashed != password
    assert auth.verify_password(password, hashed)

# ==========================
# Tests création token JWT
# ==========================
def test_create_access_token():
    data = {"sub": "alice"}
    token = auth.create_access_token(data)
    decoded = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    assert decoded["sub"] == "alice"

# ==========================
# Test FastAPI /get_current_user
# ==========================
def test_get_current_user_with_token():
    # Création d'un user fake dans DB
    db = next(override_get_db())
    user = models.User(username="alice", password_hash=auth.get_password_hash("pass"), role="admin", is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = auth.create_access_token({"sub": user.username})
    
    # Décodage manuel pour tester dépendance
    current_user = auth.get_current_user(token=token, db=db)
    assert current_user.username == "alice"
    assert current_user.role == "admin"

# ==========================
# Test rôles admin/staff
# ==========================
def test_role_checks():
    db = next(override_get_db())
    admin_user = models.User(username="admin1", password_hash=auth.get_password_hash("pass"), role="admin", is_active=True)
    staff_user = models.User(username="staff1", password_hash=auth.get_password_hash("pass"), role="staff", is_active=True)
    db.add_all([admin_user, staff_user])
    db.commit()
    db.refresh(admin_user)
    db.refresh(staff_user)

    # admin ok
    assert auth.get_current_admin(admin_user) == admin_user
    with pytest.raises(Exception):
        auth.get_current_admin(staff_user)

    # staff/admin ok
    assert auth.get_current_staff_or_admin(admin_user) == admin_user
    assert auth.get_current_staff_or_admin(staff_user) == staff_user
