-- Cambiar a la base de datos de autenticación de bots
\c bot_auth_db;

-- ╭──────────────────────────────────────────────────────╮
-- │ 📚 1. Catálogos principales (entidades puras)        │
-- ╰──────────────────────────────────────────────────────╯

-- Roles de empleados
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Permisos que puede tener un usuario de bot
CREATE TABLE bot_user_permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Estados de los modelos de bots (en desarrollo, en producción)
CREATE TABLE bot_model_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Estados de los bots (operativo, apagado, etc.)
CREATE TABLE bot_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Entornos donde corren los bots (producción, desarrollo, etc.)
CREATE TABLE bot_environments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Categorías funcionales para los bots (monitoreo, ventas, etc.)
CREATE TABLE bot_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Estados posibles para una suscripción de bot
CREATE TABLE subscription_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255)
);

-- Periodos de facturación para las suscripciones (mensual, anual, etc.)
CREATE TABLE subscription_periods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Estados posibles para los pagos de suscripciones
CREATE TABLE payment_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- ╭──────────────────────────────────────────────────────╮
-- │ 🏢 2. Empresas y empleados                           │
-- ╰──────────────────────────────────────────────────────╯

-- Empresas clientes
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    website VARCHAR(100),
    country VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    address VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Empleados que pertenecen a una empresa
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    second_last_name VARCHAR(50),
    mobile_phone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    position VARCHAR(50),
    role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- ╭──────────────────────────────────────────────────────╮
-- │ ☎️ 3. Contacto de la empresa                         │
-- ╰──────────────────────────────────────────────────────╯

-- Contactos principales de las empresas (empleados)
CREATE TABLE company_contacts (
    id SERIAL PRIMARY KEY,
    is_primary BOOLEAN DEFAULT FALSE,
    notes TEXT,
    employee_id INTEGER UNIQUE NOT NULL REFERENCES employees(id) ON DELETE CASCADE
);

-- ╭──────────────────────────────────────────────────────╮
-- │ 🤖 4. Modelos de bots y bots                         │
-- ╰──────────────────────────────────────────────────────╯

-- Modelos funcionales de bots
CREATE TABLE bot_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    version VARCHAR(50) NOT NULL,
    status_id INTEGER REFERENCES bot_model_statuses(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Bots desplegados en producción o desarrollo
CREATE TABLE bots (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    api_url VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_ping TIMESTAMP WITH TIME ZONE,
    request_per_minute INTEGER DEFAULT 0,
    data JSONB,
    bot_model_id INTEGER NOT NULL REFERENCES bot_models(id) ON DELETE CASCADE,
    status_id INTEGER REFERENCES bot_statuses(id) ON DELETE SET NULL,
    environment_id INTEGER REFERENCES bot_environments(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- ╭──────────────────────────────────────────────────────╮
-- │ 🔐 5. Credenciales de bots                           │
-- ╰──────────────────────────────────────────────────────╯

-- Credenciales cifradas asociadas a un bot
CREATE TABLE bot_credentials (
    id SERIAL PRIMARY KEY,
    hashed_password VARCHAR(255) NOT NULL,
    hashed_telegram_bot_token VARCHAR(255),
    hashed_api_access_token VARCHAR(255),
    bot_id INTEGER UNIQUE NOT NULL REFERENCES bots(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- ╭──────────────────────────────────────────────────────╮
-- │ 🙋 6. Usuarios que interactúan con bots              │
-- ╰──────────────────────────────────────────────────────╯

-- Usuarios de bot (empleados que usan los bots)
CREATE TABLE bot_users (
    id SERIAL PRIMARY KEY,
    telegram_username VARCHAR(50) UNIQUE NOT NULL,
    telegram_user_id BIGINT UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    employee_id INTEGER UNIQUE NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    permissions_id INTEGER REFERENCES bot_user_permissions(id) ON DELETE SET NULL
);

-- ╭──────────────────────────────────────────────────────╮
-- │ 🔗 7. Relación bots ↔ categorías                     │
-- ╰──────────────────────────────────────────────────────╯

-- Relación muchos a muchos entre bots y categorías
CREATE TABLE bot_category_link (
    bot_id INTEGER REFERENCES bots(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES bot_categories(id) ON DELETE CASCADE,
    PRIMARY KEY (bot_id, category_id)
);

-- ╭──────────────────────────────────────────────────────╮
-- │ 🔗 8. Relación usuarios ↔ bots                       │
-- ╰──────────────────────────────────────────────────────╯

-- Relación muchos a muchos entre usuarios y bots
CREATE TABLE user_bot_link (
    user_id INTEGER REFERENCES bot_users(id) ON DELETE CASCADE,
    bot_id INTEGER REFERENCES bots(id) ON DELETE CASCADE,
    can_access BOOLEAN DEFAULT TRUE,
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    revoked_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (user_id, bot_id)
);

-- ╭──────────────────────────────────────────────────────╮
-- │ 🔄 9. Suscripciones                                  │
-- ╰──────────────────────────────────────────────────────╯

-- Suscripciones de empresas a bots
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    is_active BOOLEAN DEFAULT TRUE,
    max_users INTEGER DEFAULT 1,
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE,
    next_payment_date TIMESTAMP WITH TIME ZONE,
    last_payment_date TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    bot_id INTEGER NOT NULL REFERENCES bots(id) ON DELETE CASCADE,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    status_id INTEGER REFERENCES subscription_statuses(id) ON DELETE SET NULL,
    subscription_period_id INTEGER REFERENCES subscription_periods(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    CONSTRAINT uq_bot_company UNIQUE (bot_id, company_id)
);

-- ╭──────────────────────────────────────────────────────╮
-- │ 💰 10. Pagos de suscripciones                        │
-- ╰──────────────────────────────────────────────────────╯

-- Pagos realizados para las suscripciones
CREATE TABLE subscription_payments (
    id SERIAL PRIMARY KEY,
    amount FLOAT DEFAULT 0.0,
    payment_date TIMESTAMP WITH TIME ZONE,
    payment_method VARCHAR(50),
    transaction_id VARCHAR(100) UNIQUE NOT NULL,
    payment_status_id INTEGER REFERENCES payment_statuses(id) ON DELETE SET NULL,
    subscription_id INTEGER NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE
);