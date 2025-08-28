from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, crud, deps

router = APIRouter()

@router.get("/", response_model=list[schemas.SessionOut])
def list_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud.get_sessions(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.SessionOut)
def create_session(session: schemas.SessionCreate, db: Session = Depends(deps.get_db)):
    return crud.create_session(db, session)

@router.put("/{session_id}", response_model=schemas.SessionOut)
def update_session(session_id: int, session_update: schemas.SessionUpdate, db: Session = Depends(deps.get_db)):
    return crud.update_session(db, session_id, session_update)

@router.delete("/{session_id}", status_code=204)
def delete_session(session_id: int, db: Session = Depends(deps.get_db)):
    crud.delete_session(db, session_id)
