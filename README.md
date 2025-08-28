CaptivePortal

Backend FastAPI + Portail Captif Wi-Fi + Admin/Staff Management

Description

CaptivePortal est une solution légère pour créer un point d’accès Wi-Fi sécurisé avec :

Gestion des utilisateurs Admin / Staff avec JWT

Gestion des clients Wi-Fi avec quotas (temps / data) et expiration

Enregistrement automatique des sessions

Portail captif web responsive pour login clients

Docker + Nginx pour déploiement rapide

Compatible CI/CD pour tests et mise en production

Structure du projet
CaptivePortal/
├─ app/                       # Backend FastAPI
│  ├─ pyproject.toml
│  ├─ .env
│  ├─ .env.example
│  ├─ main.py
│  ├─ deps.py
│  ├─ auth.py
│  ├─ models.py
│  ├─ crud.py
│  ├─ schemas.py
│  └─ routers/
│     ├─ users.py
│     ├─ clients.py
│     ├─ sessions.py
│     └─ portal.py
│
├─ web/                       # Frontend du portail captif
│  ├─ index.html
│  ├─ welcome.html
│  ├─ style.css
│  └─ login.js
│
├─ host/                      # Scripts & configs hotspot Linux
│  ├─ hostapd.conf
│  ├─ dnsmasq.conf
│  ├─ nodogsplash.conf
│  ├─ setup_captive_portal.sh
│  └─ ndsctl_deauth.sh
│
├─ nginx/                     # Reverse proxy Nginx (optionnel)
│  ├─ Dockerfile
│  └─ nginx.conf
│
├─ docker-compose.dev.yml
├─ docker-compose.prod.yml
├─ .gitignore
└─ README.md

Prérequis

Python 3.11+

Poetry (recommandé)

Docker & Docker Compose (pour tests prod ou multi-service)

Linux pour le hotspot (hostapd, dnsmasq, nodogsplash)

Installation et environnement local
1. Cloner le projet
git clone <url_du_projet>
cd CaptivePortal

2. Créer l’environnement virtuel avec Poetry
# Installer les dépendances et créer l'environnement isolé
poetry install

# Activer l'environnement
poetry shell

3. Configurer .env

Copier .env.example vers .env et éditer les variables :

cp app/.env.example app/.env
nano app/.env


Variables importantes :

DB_HOST=localhost
DB_PORT=5432
DB_NAME=captiveportal
DB_USER=postgres
DB_PASSWORD=postgres
SECRET_KEY=super-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

4. Lancer le backend FastAPI (dev)
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

5. Accéder au portail captif

Ouvrir : http://127.0.0.1:8000/ → Page de test API
Ouvrir le portail web : web/index.html

Déploiement avec Docker Compose
Développement
docker-compose -f docker-compose.dev.yml up --build

Production (Nginx + Backend + PostgreSQL)
docker-compose -f docker-compose.prod.yml up -d --build

CI/CD (GitHub Actions)

Tests automatiques avec pytest

Build Docker et déploiement automatique

Utilise Poetry pour gérer les dépendances

Exemple de workflow : .github/workflows/ci-cd.yml

Administration

Admin par défaut (à changer) :

Username : admin

Password : admin123

Possibilité de créer :

Staff

Clients avec quotas et expiration

Routes protégées avec JWT

Technologies

Backend : FastAPI, SQLAlchemy, Pydantic

Base de données : PostgreSQL

Frontend : HTML / CSS / JS simple

Docker + Nginx

CI/CD : GitHub Actions / Poetry

License

MIT License