-- Rôles de base
CREATE TYPE user_role AS ENUM ('admin','staff');
CREATE TYPE plan_type AS ENUM ('time','data','unlimited');


CREATE TABLE users (
id SERIAL PRIMARY KEY,
username TEXT UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
role user_role NOT NULL,
is_active BOOLEAN NOT NULL DEFAULT TRUE,
created_at TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE clients (
id SERIAL PRIMARY KEY,
username TEXT UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
plan_type plan_type NOT NULL,
quota_seconds INTEGER,
quota_bytes BIGINT,
expires_at TIMESTAMP,
is_active BOOLEAN NOT NULL DEFAULT TRUE,
created_at TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE sessions (
id SERIAL PRIMARY KEY,
client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
mac TEXT,
ip INET,
start_at TIMESTAMP NOT NULL DEFAULT NOW(),
end_at TIMESTAMP,
bytes_up BIGINT NOT NULL DEFAULT 0,
bytes_down BIGINT NOT NULL DEFAULT 0
);


CREATE TABLE events (
id SERIAL PRIMARY KEY,
actor_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
actor_client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
action TEXT NOT NULL,
meta JSONB,
created_at TIMESTAMP NOT NULL DEFAULT NOW()
);


-- Admin par défaut (username: admin / mot de passe: admin123, à changer)
INSERT INTO users (username, password_hash, role) VALUES (
'admin',
'$2y$12$qfTg6vR3o2xV5nW0oQ2VROwO0g2m8b1n1jzErU3KJwP5aI8H0QxK2', -- bcrypt("admin123") placeholder
'admin'
);