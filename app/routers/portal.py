from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models, schemas, crud, deps, auth

router = APIRouter()

@router.post("/login")
def client_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    client = crud.get_client_by_username(db, form_data.username)
    if not client or not auth.verify_password(form_data.password, client.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Vérifier expiration
    if client.expires_at and client.expires_at < datetime.utcnow():
        raise HTTPException(status_code=403, detail="Account expired")

    # Vérifier quota
    if client.plan_type != "unlimited" and ((client.quota_seconds and client.quota_seconds <= 0) or (client.quota_bytes and client.quota_bytes <= 0)):
        raise HTTPException(status_code=403, detail="Quota exhausted")

    # Créer session active
    session = crud.create_session(db, schemas.SessionCreate(client_id=client.id))
    return {"msg": "Login successful", "session_id": session.id}
