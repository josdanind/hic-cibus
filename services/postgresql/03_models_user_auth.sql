-- Cambiar a la base de datos de autenticación de usuarios
\c user_auth_db;

-- ╭──────────────────────────────────────────────────────╮
-- │ 📚 1. Datos Personales                               │
-- ╰──────────────────────────────────────────────────────╯

-- Información personal de usuarios
CREATE TABLE person_data (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    second_last_name VARCHAR(50),
    mobile_phone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- ╭──────────────────────────────────────────────────────╮
-- │ 🔒 2. Usuarios del sistema (CRUD Users)              │
-- ╰──────────────────────────────────────────────────────╯

-- Usuarios de la plataforma (CRUD)
CREATE TABLE crud_user (
    id SERIAL PRIMARY KEY,
    telegram_username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    data JSONB,
    person_id INTEGER UNIQUE NOT NULL REFERENCES person_data(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- ╭──────────────────────────────────────────────────────╮
-- │ 🛡️ 3. Roles de usuarios                              │
-- ╰──────────────────────────────────────────────────────╯

-- Roles que pueden asignarse a usuarios (CRUD Users)
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- ╭──────────────────────────────────────────────────────╮
-- │ 🔗 4. Relación M:N entre usuarios y roles            │
-- ╰──────────────────────────────────────────────────────╯

-- Relación muchos a muchos entre usuarios y roles
CREATE TABLE role_user_link (
    crud_user_id INTEGER REFERENCES crud_user(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (crud_user_id, role_id)
);
