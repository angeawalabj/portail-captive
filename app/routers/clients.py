from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, crud, deps

router = APIRouter()

@router.post("/", response_model=schemas.ClientOut)
def create_client(client: schemas.ClientCreate, db: Session = Depends(deps.get_db)):
    db_client = crud.get_client_by_username(db, username=client.username)
    if db_client:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_client(db, client)

@router.get("/", response_model=list[schemas.ClientOut])
def list_clients(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud.get_clients(db, skip=skip, limit=limit)

@router.get("/{client_id}", response_model=schemas.ClientOut)
def get_client(client_id: int, db: Session = Depends(deps.get_db)):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=schemas.ClientOut)
def update_client(client_id: int, client_update: schemas.ClientUpdate, db: Session = Depends(deps.get_db)):
    return crud.update_client(db, client_id, client_update)

@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(deps.get_db)):
    crud.delete_client(db, client_id)
