-- Cambiar a la base de datos de autenticación de usuarios MQTT
\c mqtt_auth_db;

-- ╭──────────────────────────────────────────────────────╮
-- │ 👥 1. MQTT Users                                     │
-- ╰──────────────────────────────────────────────────────╯
CREATE TABLE mqtt_user (
    id serial PRIMARY KEY,
    username text NOT NULL UNIQUE,
    password_hash  text NOT NULL,
    salt text NOT NULL,
    is_superuser boolean DEFAULT false,
    created timestamp with time zone DEFAULT NOW()
);