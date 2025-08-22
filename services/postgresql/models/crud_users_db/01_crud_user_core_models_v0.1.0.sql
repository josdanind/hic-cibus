-- crud_user_core_models_v0.1.0
-- ==========================================
-- 💾 CODE: CRUD_USER_CORE_MODELS
-- 📌 VERSIÓN: v0.1.0
-- 📦 DESCRIPCIÓN:
--      Modelos base del núcleo de datos para
--      el manejo de usuarios CRUD.
-- 📅 FECHA: 2025-09-10
-- ==========================================

-- ╭──────────────────────────────────────────────────────╮
-- │ 💼 1. Job Positions                                  │
-- ╰──────────────────────────────────────────────────────╯
CREATE TABLE job_positions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);


-- ╭──────────────────────────────────────────────────────╮
-- │ 🛡️ 2. Access Roles                                   │
-- ╰──────────────────────────────────────────────────────╯
CREATE TABLE access_roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);
-- Índices para acelerar búsquedas
CREATE INDEX idx_access_roles_name ON access_roles (name);


-- ╭──────────────────────────────────────────────────────╮
-- │ 👥 3. Employees                                      │
-- ╰──────────────────────────────────────────────────────╯
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    telegram_username VARCHAR(50) NOT NULL UNIQUE,
    telegram_chat_id BIGINT UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    second_last_name VARCHAR(50),
    mobile_phone VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(50) NOT NULL UNIQUE,
    job_position_id INTEGER REFERENCES job_positions(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);
-- Índices para acelerar búsquedas
CREATE INDEX idx_employees_last_name ON employees (last_name);
CREATE INDEX idx_employees_telegram_username ON employees (telegram_username);
CREATE INDEX idx_employees_telegram_chat_id ON employees (telegram_chat_id);
CREATE INDEX idx_employees_email ON employees (email);


-- ╭──────────────────────────────────────────────────────╮
-- │ 👤 4. Crud Users                                     │
-- ╰──────────────────────────────────────────────────────╯
CREATE TABLE crud_users (
    id SERIAL PRIMARY KEY,
    hashed_password VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    data JSONB,
    access_role_id INTEGER REFERENCES access_roles(id) ON DELETE SET NULL,
    employee_id INTEGER NOT NULL UNIQUE REFERENCES employees(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);
-- Índices para acelerar búsquedas
CREATE INDEX idx_crud_users_is_active ON crud_users (is_active);

-- ╭──────────────────────────────────────────────────────╮
-- │ 🤖 5. Bot Users                                      │
-- ╰──────────────────────────────────────────────────────╯
CREATE TABLE bot_users (
    id SERIAL PRIMARY KEY,
    is_active BOOLEAN NOT NULL DEFAULT true,
    data JSONB,
    access_role_id INTEGER REFERENCES access_roles(id) ON DELETE SET NULL,
    employee_id INTEGER NOT NULL UNIQUE REFERENCES employees(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);
-- Índices para acelerar búsquedas
CREATE INDEX idx_bot_users_is_active ON bot_users (is_active);