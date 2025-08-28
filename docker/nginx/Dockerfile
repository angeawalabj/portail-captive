FROM python:3.11-slim
WORKDIR /app


# Dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential curl \
&& rm -rf /var/lib/apt/lists/*


COPY app/pyproject.toml /app/
RUN pip install --no-cache-dir uv
RUN uv pip install --system -r <(pipx run poetry export -f requirements.txt --without-hashes || echo fastapi uvicorn[standard] sqlalchemy psycopg2-binary python-dotenv bcrypt pydantic-settings)


# Fallback simple si pas de Poetry :
RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy psycopg2-binary bcrypt python-dotenv pydantic pydantic-settings


COPY app /app


EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]