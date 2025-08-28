from fastapi import FastAPI
from .routers import users, clients, sessions, portal

app = FastAPI(title="Captive Portal API")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(portal.router, prefix="/portal", tags=["portal"])
