CREATE USER alarm_user WITH PASSWORD 'alarm_password';
CREATE DATABASE alarm_platform OWNER alarm_user;

\connect alarm_platform;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS devices (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS alarms (
  id SERIAL PRIMARY KEY,
  device_id INT NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  trigger_threshold NUMERIC NOT NULL DEFAULT 0,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS alarm_events (
  id SERIAL PRIMARY KEY,
  alarm_id INT NOT NULL REFERENCES alarms(id) ON DELETE CASCADE,
  event_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  status TEXT NOT NULL DEFAULT 'triggered',
  message TEXT NOT NULL
);

INSERT INTO users (name, email, password_hash)
VALUES ('Platform Owner', 'owner@example.com', gen_random_uuid()::text)
ON CONFLICT (email) DO NOTHING;

INSERT INTO devices (user_id, name, type, status)
SELECT id, 'Main Gateway', 'gateway', 'active' FROM users WHERE email = 'owner@example.com'
ON CONFLICT DO NOTHING;

INSERT INTO alarms (device_id, title, severity, trigger_threshold, is_active)
SELECT d.id, 'Temperature Spike', 'high', 75, TRUE FROM devices d JOIN users u ON d.user_id = u.id WHERE u.email = 'owner@example.com'
ON CONFLICT DO NOTHING;

-- Ensure objects are owned by the application user and grant necessary privileges
REASSIGN OWNED BY postgres TO alarm_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO alarm_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO alarm_user;
