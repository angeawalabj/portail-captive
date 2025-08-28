from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .routers import users, clients, sessions, portal
from . import deps, models

# =========================
# INITIALISATION APP
# =========================
app = FastAPI(
    title="CaptivePortal API",
    description="Backend pour Captive Portal avec gestion admin/staff et quotas clients",
    version="1.0.0"
)

# CORS (adapter si front séparé)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod, mettre le domaine exact
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CREATE TABLES IF NOT EXISTS
# =========================
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=deps.engine)

# =========================
# ROUTERS
# =========================
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(portal.router, prefix="/portal", tags=["portal"])

# =========================
# ROUTE DE TEST
# =========================
@app.get("/")
def root():
    return {"msg": "Captive Portal Backend is running"}
