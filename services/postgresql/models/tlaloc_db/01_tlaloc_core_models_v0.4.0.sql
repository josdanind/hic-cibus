-- tlaloc_core_models_v0.4.0.sql
-- ==========================================
-- 💾 CODE: TLALOC_CORE_MODELS
-- 📌 VERSIÓN: v0.4.0
-- 📦 DESCRIPCIÓN:
--      Modelos base del núcleo de datos de
--      Tlaloc
-- 📅 FECHA: 2026-01-15
-- ==========================================

-- ╭──────────────────────────────────────────────────────╮
-- │ ⚡️⚡️ 1. Triggers y funciones relacionadas ⚡️⚡️       │
-- ╰──────────────────────────────────────────────────────╯

-- ⏱️ Función de auditoría: actualiza el campo updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    ----------------------------------------------------------------
    -- NEW aún contiene los valores que el cliente envía.
    -- Si son idénticos a OLD, nada realmente cambió.
    ----------------------------------------------------------------
    IF NEW IS DISTINCT FROM OLD THEN      -- requiere PostgreSQL 9.5+
        NEW.updated_at := now();          -- marca la modificación
        RETURN NEW;                       -- continúa el UPDATE
    ELSE
        RETURN OLD;                       -- anula el UPDATE → no re‑escribe
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 🔒 Función de validación: el grupo debe tener un tipo agrupable
CREATE OR REPLACE FUNCTION f_group_requires_groupable_type()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM subprocess_types
        WHERE id = NEW.subprocess_type_id
            AND is_groupable
    ) THEN
        RAISE EXCEPTION
            'El tipo de subproceso % no permite agrupación (is_groupable = FALSE)',
            NEW.subprocess_type_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 🔎 Coherencia grupo ↔ subproceso  (proceso + tipo)
CREATE OR REPLACE FUNCTION f_subprocess_group_must_match_type()
RETURNS TRIGGER AS $$
DECLARE
    v_group_type        SMALLINT;
    v_group_process_id  BIGINT;
BEGIN
    /* Sin grupo asignado → sin validación */
    IF NEW.group_id IS NULL THEN
        RETURN NEW;
    END IF;

    /* Recupera tipo y proceso del grupo */
    SELECT subprocess_type_id,
            process_id
    INTO v_group_type,
            v_group_process_id
    FROM subprocess_groups
    WHERE id = NEW.group_id;

    /* Grupo inexistente */
    IF v_group_type IS NULL THEN
        RAISE EXCEPTION
            'Grupo % inexistente',
            NEW.group_id;
    END IF;

    /* 1️⃣ El grupo debe pertenecer al mismo proceso */
    IF v_group_process_id <> NEW.process_id THEN
        RAISE EXCEPTION
            'El grupo % pertenece al proceso %, pero el subproceso está en el proceso %',
            NEW.group_id, v_group_process_id, NEW.process_id;
    END IF;

    /* 2️⃣ El tipo debe coincidir */
    IF v_group_type <> NEW.subprocess_type_id THEN
        RAISE EXCEPTION
            'Subproceso de tipo % no puede unirse a grupo de tipo %',
            NEW.subprocess_type_id, v_group_type;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 🔗 Coherencia bot_user ↔ subscription ↔ company
CREATE OR REPLACE FUNCTION f_busl_must_match_company()
RETURNS TRIGGER AS $$
DECLARE
    v_ok BOOLEAN;
BEGIN
    SELECT TRUE
        INTO v_ok
        FROM bot_users          bu
        JOIN employees          e  ON e.id = bu.employee_id
        JOIN subscriptions      s  ON s.id = NEW.subscription_id
    WHERE bu.id      = NEW.bot_user_id
        AND e.company_id = s.company_id
    FOR SHARE;   -- ó  FOR UPDATE  si prefiere un bloqueo más fuerte

    /* Si no hay coincidencia, la consulta no devuelve filas → v_ok = NULL */
    IF NOT FOUND THEN
        RAISE EXCEPTION
            'Incoherencia de empresa: el bot_user % y la suscripción % pertenecen a compañías distintas',
            NEW.bot_user_id, NEW.subscription_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- ╭──────────────────────────────────────────────────────╮
-- │ 📚 1. Catálogos base (sin dependencias)              │
-- ╰──────────────────────────────────────────────────────╯

/*───────────────────────────────────────────────────────────────┐
│ 1. 🤖 bot_model_statuses                                       │
│ Catálogo de estados de desarrollo de un modelo de bot          │
│ (p. ej. EN_DESARROLLO, EN_PRODUCCION).                         │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_model_statuses (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                                 NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                                NOT NULL
                    CHECK ( char_length(TRIM(name)) > 0 ),

    description     TEXT,

    is_active       BOOLEAN                                     NOT NULL DEFAULT TRUE,

    -- Auditoría
    created_at      TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER bot_model_statuses_set_updated_at
BEFORE UPDATE ON bot_model_statuses
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 2. 🤖 bot_statuses                                             │
│ Catálogo de estados operativos que puede tener un bot          │
│ (p. ej. ONLINE, OFFLINE, ERROR).                               │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_statuses (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                               NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                              NOT NULL UNIQUE
                    CHECK ( char_length(TRIM(name)) > 0 ),

    description     TEXT,

    is_active       BOOLEAN                                   NOT NULL DEFAULT TRUE,

    -- Auditoría
    created_at      TIMESTAMPTZ                               NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                               NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER bot_statuses_set_updated_at
BEFORE UPDATE ON bot_statuses
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 3. 🧩 process_templates                                        │
│ Catálogo de plantillas estandarizadas de procesos operativos   │
│ (p. ej. GERMINACION, RIEGO_ZONAL, TESTEO_MATERAS).             │
│ Cada plantilla describe la lógica funcional común a múltiples  │
│ procesos implementados en distintas unidades operativas.       │
└───────────────────────────────────────────────────────────────*/

CREATE TABLE process_templates (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                                 NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                                NOT NULL
                    CHECK (char_length(TRIM(name)) > 0),


    -- ¿Es un proceso en fase experimental?
    is_experimental BOOLEAN                                     NOT NULL DEFAULT FALSE,

    -- Estado general de la plantilla
    is_active       BOOLEAN                                     NOT NULL DEFAULT TRUE,

    description     TEXT                                        NULL,

    -- Auditoría
    created_at      TIMESTAMPTZ NOT NULL                        DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL                        DEFAULT now()
);

-- 🔄 Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER process_templates_set_updated_at
BEFORE UPDATE ON process_templates
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 4. 🌐 bot_environments                                         │
│ Catálogo de entornos donde puede ejecutarse un bot             │
│ (p. ej. PRODUCCION, DESARROLLO, PRUEBAS).                      │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_environments (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                               NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                              NOT NULL
                    CHECK (
                        char_length(TRIM(name)) > 0
                    ),

    description     TEXT,

    is_active       BOOLEAN                                   NOT NULL DEFAULT TRUE,

    -- Auditoría
    created_at      TIMESTAMPTZ                               NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                               NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER bot_environments_set_updated_at
BEFORE UPDATE ON bot_environments
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 5. 🗂️ bot_categories                                           │
│ Catálogo de categorías funcionales de los bots                 │
│ (p. ej. MONITOREO, AUTOMATIZACION).                            │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_categories (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                                     NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                                    NOT NULL
                    CHECK ( char_length(TRIM(name)) > 0 ),

    description     TEXT,

    -- Auditoría
    created_at      TIMESTAMPTZ                                     NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                                     NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER bot_categories_set_updated_at
BEFORE UPDATE ON bot_categories
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*──────────────────────────────────────────────────────────────────────────┐
│ 6. 📏 magnitudes                                                          │
│ Catálogo de magnitudes físicas que los bots pueden medir o controlar      │
│ (p. ej. TEMPERATURA, HUMEDAD, LUZ).                                       │
└──────────────────────────────────────────────────────────────────────────*/
CREATE TABLE magnitudes (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                                 NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                                NOT NULL UNIQUE
                    CHECK (char_length(TRIM(name)) > 0),

    unit            VARCHAR(20)                                 NOT NULL
                    CHECK (unit ~ '^[A-Za-z/_-]{1,20}$'),


    symbol          VARCHAR(10)                                 NOT NULL
                    CHECK (symbol ~ '^[^\\s]{1,10}$'),

    description     TEXT                                        NULL,

    -- Precisión de lectura/control
    decimal_places  SMALLINT                                    NOT NULL DEFAULT 2
                    CHECK (decimal_places BETWEEN 0 AND 6),

    -- Auditoría
    created_at      TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER magnitudes_set_updated_at
BEFORE UPDATE ON magnitudes
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 7. 🏭 manufacturers                                            │
│ Catálogo de fabricantes de hardware utilizado en los procesos  │
│ (p. ej. MICROCHIP, BOSCH, TEXAS_INSTRUMENTS).                  │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE manufacturers (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                                 NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                                NOT NULL UNIQUE
                    CHECK (char_length(TRIM(name)) > 0),

    -- Datos de contacto
    website         VARCHAR(255)                                NULL
                    CHECK (
                        website IS NULL
                        OR website ~* '^(https?|ftp)://'
                    ),

    description     TEXT                                        NULL,

    -- Auditoría
    created_at      TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER manufacturers_set_updated_at
BEFORE UPDATE ON manufacturers
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 8. 🗓️ subscription_statuses                                    │
│ Catálogo de estados posibles de una suscripción                │
│ (p. ej. ACTIVA, GRACE_PERIOD, CANCELADA).                      │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE subscription_statuses (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                               NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                              NOT NULL
                    CHECK (char_length(TRIM(name)) > 0),

    description     TEXT,

    is_active       BOOLEAN                                   NOT NULL DEFAULT TRUE,

    -- Auditoría
    created_at      TIMESTAMPTZ                               NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                               NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER subscription_statuses_set_updated_at
BEFORE UPDATE ON subscription_statuses
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 9. ⏳ period_units                                             │
│ Catálogo de unidades de tiempo para los periodos de facturación│
│ (p. ej. MENSUAL, ANUAL).                                       │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE period_units (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                               NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    -- Nombres localizados
    name_es         VARCHAR(100)                              NOT NULL UNIQUE
                    CHECK (char_length(TRIM(name_es)) > 0),

    description     TEXT,

    -- Auditoría
    created_at      TIMESTAMPTZ                               NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                               NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER period_units_set_updated_at
BEFORE UPDATE ON period_units
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 10. 💸 invoice_statuses                                        │
│ Catálogo de estados que puede tener una factura emitida        │
│ (p. ej. PENDING, PAID, OVERDUE).                               │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE invoice_statuses (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                               NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                              NOT NULL
                    CHECK (char_length(TRIM(name)) > 0),

    description     TEXT,

    is_active       BOOLEAN                                   NOT NULL DEFAULT TRUE,

    -- Auditoría
    created_at      TIMESTAMPTZ                               NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                               NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER invoice_statuses_set_updated_at
BEFORE UPDATE ON invoice_statuses
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 11. 💳 payment_statuses                                        │
│ Catálogo de estados posibles para un pago o intento de pago    │
│ (p. ej. SUCCEEDED, FAILED, PENDING).                           │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE payment_statuses (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                               NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                              NOT NULL
                    CHECK (char_length(TRIM(name)) > 0),

    description     TEXT,

    is_active       BOOLEAN                                   NOT NULL DEFAULT TRUE,

    -- Auditoría
    created_at      TIMESTAMPTZ                               NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                               NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER payment_statuses_set_updated_at
BEFORE UPDATE ON payment_statuses
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 12. 💳 payment_methods                                         │
│ Catálogo de métodos de pago aceptados                          │
│ (p. ej. BANK_TRANSFER, CREDIT_CARD, NEQUI).                    │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE payment_methods (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                               NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                              NOT NULL
                    CHECK (char_length(TRIM(name)) > 0),

    description     TEXT,

    is_active       BOOLEAN                                   NOT NULL DEFAULT TRUE,

    -- Auditoría
    created_at      TIMESTAMPTZ                               NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                               NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER payment_methods_set_updated_at
BEFORE UPDATE ON payment_methods
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 13. 🔐 user_process_permissions                                │
│ Catálogo de permisos que pueden tener los usuarios             │
│ para ejecutar acciones en procesos (p. ej. READ_TELEMETRY,     │
│ START_PROCESS).                                                │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE user_process_permissions (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                               NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                              NOT NULL
                    CHECK (char_length(TRIM(name)) > 0),

    description     TEXT,

    -- Auditoría
    created_at      TIMESTAMPTZ                               NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                               NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER user_process_permissions_set_updated_at
BEFORE UPDATE ON user_process_permissions
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 14. 🤖 bot_process_permissions                                 │
│ Catálogo de permisos que pueden tener los bots                 │
│ para ejecutar acciones en procesos (p. ej. READ_TELEMETRY,     │
│ START_PROCESS).                                                │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_process_permissions (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                               NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                              NOT NULL
                    CHECK (char_length(TRIM(name)) > 0),

    description     TEXT,

    -- Auditoría
    created_at      TIMESTAMPTZ                               NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                               NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER bot_process_permissions_set_updated_at
BEFORE UPDATE ON bot_process_permissions
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 15. 👥 roles                                                   │
│ Catálogo de roles de usuario dentro del sistema                │
│ (p. ej. ADMIN, USER, GUEST).                                   │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE roles (
    -- Clave primaria
    id              SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                               NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                              NOT NULL
                    CHECK (char_length(TRIM(name)) > 0),

    description     TEXT,

    is_active       BOOLEAN                                   NOT NULL DEFAULT TRUE,

    -- Auditoría
    created_at      TIMESTAMPTZ                               NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                               NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER roles_set_updated_at
BEFORE UPDATE ON roles
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 16. 🧩 subprocess_types                                        │
│ Catálogo de tipos funcionales de subproceso. Indica si un tipo │
│ puede agruparse (is_groupable) para operar como unidad lógica. │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE subprocess_types (
    id                      BIGINT    GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code                    VARCHAR(30)                             NOT NULL UNIQUE
                            CHECK (
                                code = UPPER(TRIM(code))
                                AND code ~ '^[A-Z0-9_]{1,30}$'
                            ),

    name                    VARCHAR(100)                            NOT NULL UNIQUE
                            CHECK (char_length(TRIM(name)) > 0),

    is_active               BOOLEAN                                 NOT NULL DEFAULT TRUE,

    -- Es agrupable?
    is_groupable            BOOLEAN                                 NOT NULL DEFAULT FALSE,

    -- Es experimental?
    is_experimental         BOOLEAN                                 NOT NULL DEFAULT FALSE,

    description             TEXT,

    -- Proceso al que pertenece este tipo
    process_template_id     BIGINT
                            REFERENCES process_templates(id)        ON DELETE RESTRICT,

    -- Auditoría
    created_at              TIMESTAMPTZ                             NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ                             NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX subprocess_types_is_groupable_idx ON subprocess_types(is_groupable);
CREATE INDEX subprocess_types_is_active_idx ON subprocess_types(is_active);
CREATE INDEX subprocess_types_is_experimental_idx ON subprocess_types(is_experimental);
CREATE INDEX subprocess_types_process_templates_idx ON subprocess_types(process_template_id);

-- Trigger de auditoría: mantiene updated_at en cada UPDATE
CREATE TRIGGER subprocess_types_set_updated_at
BEFORE UPDATE ON subprocess_types
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- ╭──────────────────────────────────────────────────────────────────────────────╮
-- │ 🗂️ 2. Catálogos dependientes                                                 │
-- │    (Tablas que dependen de los catálogos base, con claves foráneas,          │
-- │     relaciones y estructuras extendidas)                                     │
-- ╰──────────────────────────────────────────────────────────────────────────────╯

/*───────────────────────────────────────────────────────────────┐
│ 17. 🗓️ plans                                                   │
│ Catálogo de planes de suscripción                              │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE plans (
    id                  SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Claves de negocio
    code                VARCHAR(30)                             NOT NULL UNIQUE
                        CHECK (
                            code = UPPER(TRIM(code))
                            AND code ~ '^[A-Z0-9_]{1,30}$'
                        ),

    name                VARCHAR(100)                            NOT NULL
                        CHECK (char_length(TRIM(name)) > 0),

    description         TEXT,

    -- Información comercial
    price_period        NUMERIC(10, 2)                          NOT NULL
                        CHECK (price_period >= 0),

    currency            CHAR(3)                                 NOT NULL DEFAULT 'COP'
                        CHECK (currency ~ '^[A-Z]{3}$'),

    -- Límites
    max_users           SMALLINT                                NOT NULL DEFAULT 1
                        CHECK (max_users >= 1),

    max_processes       SMALLINT                                NOT NULL DEFAULT 1
                        CHECK (max_processes >= 1),

    max_mcus_x_process  SMALLINT                                NOT NULL DEFAULT 1
                        CHECK (max_mcus_x_process >= 1),

    -- Características extendidas
    features            JSONB                                   DEFAULT NULL,

    is_active           BOOLEAN                                 NOT NULL DEFAULT TRUE,

    -- Relaciones
    period_unit_id      SMALLINT                                NOT NULL
                        REFERENCES period_units(id)             ON DELETE RESTRICT,

    -- Auditoría
    created_at          TIMESTAMPTZ                             NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                             NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER plans_set_updated_at
BEFORE UPDATE ON plans
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 18. 🤖 bot_models                                              │
│ Catálogo de modelos de bot disponibles en el sistema           │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_models (
    id                  SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Identificación
    name                VARCHAR(100)                              NOT NULL
                        CHECK (char_length(TRIM(name)) > 0),

    version             VARCHAR(20)                               NOT NULL
                        CHECK (
                            char_length(TRIM(version)) > 0
                            AND version ~ '^[0-9]+(\.[0-9]+)*$'
                        ),

    description         TEXT,

    -- Estado del modelo
    status_id           SMALLINT
                        REFERENCES bot_model_statuses(id)         ON DELETE RESTRICT,

    -- Auditoría
    created_at          TIMESTAMPTZ                               NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                               NOT NULL DEFAULT now(),

    -- Unicidad combinada
    CONSTRAINT uq_bot_model_name_version UNIQUE (name, version)
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER bot_models_set_updated_at
BEFORE UPDATE ON bot_models
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 19. 🌡️ sensor_models                                           │
│ Catálogo de modelos de sensores disponibles en el sistema      │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE sensor_models (
    id                  SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Identificación
    name                VARCHAR(100)                                NOT NULL
                        CHECK (char_length(TRIM(name)) > 0),

    version             VARCHAR(20)                                 NULL
                        CHECK (
                            version IS NULL
                            OR (
                                char_length(TRIM(version)) > 0
                                AND version ~ '^[0-9]+(\.[0-9]+)*$'
                            )
                        ),

    description         TEXT,

    -- Relación con el fabricante
    manufacturer_id     SMALLINT REFERENCES manufacturers(id)       ON DELETE SET NULL,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),

    -- Unicidad combinada
    CONSTRAINT uq_sensor_model_name_version UNIQUE (name, version)
);

-- Índice recomendado para la clave foránea
CREATE INDEX sensor_models_mfr_idx ON sensor_models(manufacturer_id);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER sensor_models_set_updated_at
BEFORE UPDATE ON sensor_models
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 20. ⚙️ actuator_models                                         │
│ Catálogo de modelos de actuadores disponibles en el sistema    │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE actuator_models (
    id                  SMALLINT  GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Identificación
    name                VARCHAR(100)                                NOT NULL
                        CHECK (char_length(TRIM(name)) > 0),

    version             VARCHAR(20)                                 NULL
                        CHECK (
                            version IS NULL
                            OR (
                                char_length(TRIM(version)) > 0
                                AND version ~ '^[0-9]+(\.[0-9]+)*$'
                            )
                        ),

    description         TEXT,

    -- Relación con el fabricante
    manufacturer_id     SMALLINT                                    NULL
                        REFERENCES manufacturers(id)                ON DELETE SET NULL,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),

    -- Unicidad combinada
    CONSTRAINT uq_actuator_model_name_version UNIQUE (name, version)
);

-- Índice recomendado para la clave foránea
CREATE INDEX actuator_models_mfr_idx ON actuator_models(manufacturer_id);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER actuator_models_set_updated_at
BEFORE UPDATE ON actuator_models
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 21. 🕹️ controller_models                                       │
│ Catálogo de modelos de controladores disponibles en el sistema │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE controller_models (
    id                  SMALLINT  GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Identificación
    name                VARCHAR(100)                                NOT NULL
                        CHECK (char_length(TRIM(name)) > 0),

    version             VARCHAR(20)                                 NOT NULL
                        CHECK (
                            char_length(TRIM(version)) > 0
                            AND version ~ '^[0-9]+(\.[0-9]+)*$'
                        ),

    architecture        VARCHAR(50)                                 NULL
                        CHECK (
                            char_length(TRIM(architecture)) > 0
                        ),

    description         TEXT                                        NULL,

    -- Relación con el fabricante
    manufacturer_id     SMALLINT                                    NULL
                        REFERENCES manufacturers(id)                ON DELETE SET NULL,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),

    -- Unicidad combinada
    CONSTRAINT uq_controller_model_name_version UNIQUE (name, version)
);

-- Índice recomendado para la clave foránea
CREATE INDEX controller_models_mfr_idx ON controller_models(manufacturer_id);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER controller_models_set_updated_at
BEFORE UPDATE ON controller_models
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- ╭──────────────────────────────────────────────────────╮
-- │ 🏢 3. Datos maestro                                  │
-- ╰──────────────────────────────────────────────────────╯

/*───────────────────────────────────────────────────────────────┐
│ 22. 🏢 companies                                               │
│ Catálogo de empresas que utilizan los bots y servicios         │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE companies (
    id              BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Claves de negocio
    code            VARCHAR(30)                                 NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                                NOT NULL UNIQUE
                    CHECK (char_length(TRIM(name)) > 0),

    description     TEXT,

    is_active       BOOLEAN                                     NOT NULL DEFAULT TRUE,

    -- Contacto
    phone           VARCHAR(20)                                 NOT NULL UNIQUE
                    CHECK (phone ~ '^\+[1-9][0-9]{6,14}$'),   -- Formato E.164

    email           VARCHAR(100)                                NOT NULL UNIQUE
                    CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),

    website         VARCHAR(255)
                    CHECK (
                        website IS NULL
                        OR website ~* '^(https?|ftp)://'
                    ),

    -- Dirección física
    country         VARCHAR(100),
    state           VARCHAR(100),
    city            VARCHAR(100),
    zip_code        VARCHAR(20),
    address         VARCHAR(255),

    -- Auditoría
    created_at      TIMESTAMPTZ                             NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                             NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX companies_is_active_idx ON companies(is_active);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER companies_set_updated_at
BEFORE UPDATE ON companies
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 23. 👤 employees                                               │
│ Registro de empleados asociados a las empresas                 │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE employees (
    id                  BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Información personal
    first_name          VARCHAR(50)                                 NOT NULL
                        CHECK (char_length(TRIM(first_name)) > 0),

    middle_name         VARCHAR(50)
                        CHECK (
                            middle_name IS NULL
                            OR char_length(TRIM(middle_name)) > 0
                        ),

    last_name           VARCHAR(50)                                 NOT NULL
                        CHECK (char_length(TRIM(last_name)) > 0),

    second_last_name    VARCHAR(50)
                        CHECK (
                            second_last_name IS NULL
                            OR char_length(TRIM(second_last_name)) > 0
                        ),

    -- Información de contacto
    email               VARCHAR(100)                                NOT NULL UNIQUE
                        CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),

    mobile_phone        VARCHAR(16)                                 NOT NULL UNIQUE
                        CHECK (mobile_phone ~ '^\+[1-9][0-9]{6,14}$'),  -- Formato E.164

    -- Información laboral
    position            VARCHAR(100)                                NULL
                        CHECK (
                            position IS NULL
                            OR char_length(TRIM(position)) > 0
                        ),

    -- Relación con la empresa
    company_id          BIGINT                                      NOT NULL
                        REFERENCES companies(id)                    ON DELETE CASCADE,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX employees_company_idx    ON employees(company_id);
CREATE INDEX employees_last_name_idx  ON employees(last_name);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER employees_set_updated_at
BEFORE UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 24. ☎️ company_contacts                                        │
│ Contactos designados dentro de cada empresa                    │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE company_contacts (
    id              BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Atributos del contacto
    is_primary      BOOLEAN                                     NOT NULL DEFAULT FALSE,

    notes           TEXT                                        NULL,

    -- Relación 1 : 1 con empleado
    employee_id     BIGINT                                      NOT NULL UNIQUE
                    REFERENCES employees(id)
                    ON DELETE CASCADE,

    -- Auditoría
    created_at      TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Índice para búsquedas rápidas de contactos principales
CREATE INDEX company_contacts_is_primary_idx ON company_contacts(is_primary);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER company_contacts_set_updated_at
BEFORE UPDATE ON company_contacts
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 25. 🔗 employee_role_links                                     │
│ Relación muchos-a-muchos entre empleados y roles               │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE employee_role_links (
    -- Clave compuesta
    employee_id     BIGINT                                  NOT NULL
                    REFERENCES employees(id)
                    ON DELETE CASCADE,

    role_id         SMALLINT                                NOT NULL
                    REFERENCES roles(id)
                    ON DELETE CASCADE,

    -- Metadatos
    assigned_at     TIMESTAMPTZ                             NOT NULL DEFAULT now(),

    -- Auditoría
    created_at      TIMESTAMPTZ                             NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                             NOT NULL DEFAULT now(),

    -- Restricción primaria compuesta
    PRIMARY KEY (employee_id, role_id)
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER employee_role_links_set_updated_at
BEFORE UPDATE ON employee_role_links
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 26. 🤖 bots                                                    │
│ Registro de bots disponibles en el sistema                     │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bots (
    id                  INTEGER   GENERATED ALWAYS AS IDENTITY  PRIMARY KEY,

    -- Identificación
    name                VARCHAR(100)                            NOT NULL UNIQUE
                        CHECK (char_length(TRIM(name)) > 0),

    description         TEXT,

    api_url             VARCHAR(255)                            NOT NULL UNIQUE
                        CHECK (
                            char_length(TRIM(api_url)) > 0
                            AND api_url ~* '^(https?)://'
                        ),

    -- Estado y control
    is_active           BOOLEAN                                 NOT NULL DEFAULT TRUE,

    last_ping           TIMESTAMPTZ,

    request_per_minute  INTEGER                                 NOT NULL DEFAULT 0
                        CHECK (request_per_minute >= 0),

    data                JSONB                                   DEFAULT NULL,

    -- Relaciones
    bot_model_id        SMALLINT                                NOT NULL
                        REFERENCES bot_models(id)               ON DELETE CASCADE,

    status_id           SMALLINT
                        REFERENCES bot_statuses(id)             ON DELETE RESTRICT,

    environment_id      SMALLINT
                        REFERENCES bot_environments(id)         ON DELETE RESTRICT,

    -- Auditoría
    created_at          TIMESTAMPTZ                             NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                             NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX bots_is_active_idx            ON bots(is_active);
CREATE INDEX bots_request_per_minute_idx   ON bots(request_per_minute);
CREATE INDEX bots_status_idx               ON bots(status_id);
CREATE INDEX bots_bot_model_idx            ON bots(bot_model_id);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER bots_set_updated_at
BEFORE UPDATE ON bots
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 27. 🔐 bot_credentials                                         │
│ Credenciales asociadas 1 : 1 a cada bot                        │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_credentials (
    id                      INTEGER   GENERATED ALWAYS AS IDENTITY  PRIMARY KEY,

    -- Autenticación
    hashed_password         VARCHAR(255)                            NOT NULL
                            CHECK (char_length(TRIM(hashed_password)) > 0),

    hashed_api_access_token  VARCHAR(255)                           UNIQUE,

    -- Relación con el bot
    bot_id                  INTEGER                                 NOT NULL UNIQUE
                            REFERENCES bots(id) ON DELETE CASCADE,

    -- Auditoría
    created_at              TIMESTAMPTZ                             NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ                             NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER bot_credentials_set_updated_at
BEFORE UPDATE ON bot_credentials
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 28. 📝 subscriptions                                           │
│ Suscripciones de empresas a bots bajo un plan determinado      │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE subscriptions (
    id                  BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Estado y vigencia
    is_active           BOOLEAN                                     NOT NULL DEFAULT TRUE,
    start_date          TIMESTAMPTZ,
    end_date            TIMESTAMPTZ
                        CHECK (
                            end_date IS NULL
                            OR start_date IS NULL
                            OR start_date < end_date            -- Fechas coherentes
                        ),

    -- Relaciones
    bot_id              INTEGER                                     NOT NULL
                        REFERENCES bots(id)                         ON DELETE CASCADE,

    company_id          BIGINT                                      NOT NULL
                        REFERENCES companies(id)                    ON DELETE CASCADE,

    plan_id             SMALLINT                                    NOT NULL
                        REFERENCES plans(id)                        ON DELETE RESTRICT,

    status_id           SMALLINT                                    NULL
                        REFERENCES subscription_statuses(id)        ON DELETE RESTRICT,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),

    -- Unicidad bot + empresa
    CONSTRAINT uq_subscriptions_bot_company UNIQUE (bot_id, company_id)
);

-- Índices auxiliares
CREATE INDEX subscriptions_is_active_idx   ON subscriptions (is_active);
CREATE INDEX subscriptions_bot_idx         ON subscriptions (bot_id);
CREATE INDEX subscriptions_company_idx     ON subscriptions (company_id);
CREATE INDEX subscriptions_plan_idx        ON subscriptions (plan_id);
CREATE INDEX subscriptions_status_idx      ON subscriptions (status_id);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER subscriptions_set_updated_at
BEFORE UPDATE ON subscriptions
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 29. 🔗 bot_category_links                                      │
│ Relación muchos-a-muchos entre bots y sus categorías           │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_category_links (
    -- Clave compuesta
    bot_id          INTEGER                         NOT NULL
                    REFERENCES bots(id)             ON DELETE CASCADE,

    category_id     SMALLINT                        NOT NULL
                    REFERENCES bot_categories(id)   ON DELETE CASCADE,

    -- Auditoría
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    PRIMARY KEY (bot_id, category_id)
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER bot_category_links_set_updated_at
BEFORE UPDATE ON bot_category_links
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- ╭──────────────────────────────────────────────────────╮
-- │ 🌐 4. Componentes IoT y hardware físico              │
-- ╰──────────────────────────────────────────────────────╯

/*───────────────────────────────────────────────────────────────┐
│ 30. 🏗️ operational_units                                       │
│ Unidades operativas pertenecientes a una empresa               │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE operational_units (
    id              BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Información general
    code            VARCHAR(30)                                 NOT NULL UNIQUE
                    CHECK (
                        code = UPPER(TRIM(code))
                        AND code ~ '^[A-Z0-9_]{1,30}$'
                    ),

    name            VARCHAR(100)                                NOT NULL UNIQUE
                    CHECK (char_length(TRIM(name)) > 0),

    is_active       BOOLEAN                                     NOT NULL DEFAULT TRUE,

    description     TEXT,

    location        VARCHAR(255),

    -- Relación con empresa
    company_id      BIGINT                                      NOT NULL
                    REFERENCES companies(id)                    ON DELETE CASCADE,

    -- Auditoría
    created_at      TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX operational_units_company_idx   ON operational_units(company_id);
CREATE INDEX operational_units_is_active_idx ON operational_units(is_active);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER operational_units_set_updated_at
BEFORE UPDATE ON operational_units
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 31. 📊  processes                                              │
│ Procesos que se ejecutan dentro de una unidad operativa        │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE processes (
    id                  BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Información general
    code                VARCHAR(30)                                 NOT NULL UNIQUE
                        CHECK (
                            code = UPPER(TRIM(code))
                            AND code ~ '^[A-Z0-9_]{1,30}$'
                        ),

    name                VARCHAR(100)                                NOT NULL
                        CHECK (char_length(TRIM(name)) > 0),

    is_active           BOOLEAN                                     NOT NULL DEFAULT TRUE,

    is_pilot            BOOLEAN                                     NOT NULL DEFAULT FALSE,

    description         TEXT,

    -- Relación con la unidad operativa
    operational_unit_id BIGINT                                      NOT NULL
                        REFERENCES operational_units(id)            ON DELETE CASCADE,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX processes_operational_unit_idx ON processes(operational_unit_id);
CREATE INDEX processes_is_active_idx       ON processes(is_active);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER processes_set_updated_at
BEFORE UPDATE ON processes
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 32. 🎞️ reels                                                   │
│ Contenedores de los teatros                                    │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE reels (
    id                  BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Información general
    label               VARCHAR(100)                                NOT NULL
                        CHECK (char_length(TRIM(label)) > 0),

    description         TEXT,

    is_active           BOOLEAN                                     NOT NULL DEFAULT TRUE,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER reels_set_updated_at
BEFORE UPDATE ON reels
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

/*───────────────────────────────────────────────────────────────┐
│ 33. 🔗 process_reel_links                                      │
│ Relación mucho a muchos entre los procesos y contenedores      │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE process_reel_links (
    process_id          BIGINT                      NOT NULL
                        REFERENCES processes(id)
                        ON DELETE CASCADE,

    reel_id             BIGINT                      NOT NULL
                        REFERENCES reels(id)
                        ON DELETE CASCADE,

    process_alias        VARCHAR(25)                 NOT NULL,

    -- Auditoría
    created_at          TIMESTAMPTZ                 NOT NULL DEFAULT now(),

    -- Clave primaria compuesta
    PRIMARY KEY (process_id, reel_id)
);

-- ESTRUCTURA TEMPORAL HASTA DEFINIR REGLAS DE NEGOCIO
/*───────────────────────────────────────────────────────────────┐
│ 33. 🎑. frame_templates                                        │
│ Diseños de frames                                              │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE frame_templates (
    id              BIGINT          GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    name            VARCHAR(100)                                    NOT NULL,

    description     TEXT,

    -- Auditoría
    created_at      TIMESTAMPTZ                                     NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                                     NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER frame_templates_set_updated_at
BEFORE UPDATE ON frame_templates
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

/*───────────────────────────────────────────────────────────────┐
│ 34. 🔍 queries                                                 │
│ Filtros para las galerías                                      │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE queries (
    -- 🔑 PK
    id              BIGINT          GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Nombre único de la consulta
    name            VARCHAR(100)                                    NOT NULL UNIQUE
                    CHECK ( char_length(TRIM(name)) > 0 ),

    -- Plantilla SQL
    sql_template    TEXT                                            NOT NULL,

    -- Lista blanca opcional
    whitelist       JSONB,

    -- Descripción opcional
    description   TEXT,

    -- Auditoría
    created_at      TIMESTAMPTZ                                     NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ                                     NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER queries_set_updated_at
BEFORE UPDATE ON queries
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

/*───────────────────────────────────────────────────────────────┐
│ 35. 🎪 galleries                                               │
│ Galerías                                                       │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE galleries (
    -- 🔑 PK
    id                  BIGINT          GENERATED BY DEFAULT AS IDENTITY    PRIMARY KEY,

    name                VARCHAR(100)                                        NOT NULL UNIQUE
                        CHECK ( char_length(TRIM(name)) > 0 ),

    -- 📝 Descripción opcional
    description         TEXT,

    -- ⚙️ Estado
    is_active           BOOLEAN                                             NOT NULL DEFAULT TRUE,

    -- ⚙️ Configuraciones (JSONB no nulo con valor por defecto {})
    settings            JSONB           NOT NULL DEFAULT '{}'::jsonb,

    -- 🔗 Relaciones
    frame_template_id   BIGINT          NOT NULL
                                        REFERENCES frame_templates (id)  ON DELETE RESTRICT,
    query_id            BIGINT          NOT NULL
                                        REFERENCES queries (id)          ON DELETE RESTRICT,

    -- 📆 Auditoría
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER galleries_set_updated_at
BEFORE UPDATE ON galleries
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ X. 🎪 gallery_posters                                          │
│ Texto para el boton de la galería según su genero              │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE gallery_posters (
    id                      BIGINT      GENERATED BY DEFAULT AS IDENTITY    PRIMARY KEY,

    gallery_id              BIGINT      NOT NULL
                            REFERENCES galleries(id)
                            ON DELETE CASCADE,
    
    -- 🪧 Nombre del botón que lleva a la galería
    poster                  TEXT        NOT NULL,

    gender                  VARCHAR(20) NOT NULL
                            CHECK (gender IN ('male', 'female', 'neutral')),
    
    UNIQUE (gallery_id, gender)
);


/*───────────────────────────────────────────────────────────────┐
│ 36. 🎪 theaters                                                │
│ Teatros                                                        │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE theaters (
    -- 🔑 PK
    id                      BIGINT      GENERATED BY DEFAULT AS IDENTITY    PRIMARY KEY,

    -- 🧾 Código único del theater
    code                    VARCHAR(50)                                     NOT NULL UNIQUE
                            CHECK (
                                code = UPPER(TRIM(code))
                                AND code ~ '^[A-Z0-9_]{1,30}$'
                            ),

    -- 🪧 Botón principal (opcional)
    billboard               VARCHAR(15),

    -- 🖼️ URL de la imagen de portada
    cover_url               VARCHAR(255)                                    NOT NULL
                            CHECK (
                                char_length(TRIM(cover_url)) > 0
                                AND cover_url ~* '^(https?|ftp)://'
                            ),

    -- ⚙️ Estado
    is_active               BOOLEAN                                         NOT NULL DEFAULT TRUE,

    -- 🎛️ Mostrar todas las galerías asociadas
    show_all_galleries      BOOLEAN                                         NOT NULL DEFAULT FALSE,

    -- 📝 Descripción opcional
    description             TEXT,

    -- 🔗 Relaciones
    reel_id                 BIGINT      NOT NULL
                                        REFERENCES reels (id)               ON DELETE RESTRICT,
    frame_template_id       BIGINT      NOT NULL
                                        REFERENCES frame_templates (id)     ON DELETE RESTRICT,

    -- 📆 Auditoría
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now()
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER theaters_set_updated_at
BEFORE UPDATE ON theaters
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- ╭────────────────────────────────────────────────────────────────────────────╮
-- │ 37. 🔗 TABLA: theater_gallery_links                                        │
-- ╰────────────────────────────────────────────────────────────────────────────╯
CREATE TABLE theater_gallery_links (
    -- 🔗 Relaciones
    theater_id      BIGINT                          NOT NULL
                    REFERENCES theaters(id)
                    ON DELETE CASCADE,

    gallery_id      BIGINT                          NOT NULL
                    REFERENCES galleries(id)
                    ON DELETE CASCADE,

    -- 📆 Auditoría
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- 🔑 Clave primaria compuesta
    PRIMARY KEY (theater_id, gallery_id)
);

/*──────────────────────────────────────────────────────────────┐
│ 36. 🧩 subprocess_groups                                      │
│ Grupos homogéneos de subprocesos agrupables dentro de un      │
│ proceso, según su tipo (solo si is_groupable = TRUE).         │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE subprocess_groups (
    id                  BIGINT      GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,

    -- Relaciones
    subprocess_type_id  BIGINT                                      NOT NULL
                        REFERENCES subprocess_types(id)             ON DELETE RESTRICT,

    process_id          BIGINT                                      NOT NULL
                        REFERENCES processes(id)                    ON DELETE CASCADE,

    -- Información del grupo
    name                VARCHAR(100)                                NOT NULL
                        CHECK (char_length(TRIM(name)) > 0),

    description         TEXT                                        NULL,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),

    -- Restricción de unicidad compuesta
    UNIQUE (process_id, subprocess_type_id, name)
);

-- Trigger de auditoría
CREATE TRIGGER subprocess_groups_set_updated_at
BEFORE UPDATE ON subprocess_groups
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- ✅ Verificación: solo se permiten tipos agrupables
CREATE TRIGGER check_groupable_type
BEFORE INSERT OR UPDATE ON subprocess_groups
FOR EACH ROW
EXECUTE FUNCTION f_group_requires_groupable_type();


/*───────────────────────────────────────────────────────────────┐
│ 37. 🪜 subprocesses                                            │
│ Subprocesos que conforman un proceso operativo                 │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE subprocesses (
    id                      BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Información general
    code                    VARCHAR(30)                                 NOT NULL UNIQUE
                            CHECK (
                                code = UPPER(TRIM(code))
                                AND code ~ '^[A-Z0-9_]{1,30}$'
                            ),

    name                    VARCHAR(100)                                NOT NULL UNIQUE
                            CHECK (char_length(TRIM(name)) > 0),

    is_active               BOOLEAN                                     NOT NULL DEFAULT TRUE,

    is_pilot                BOOLEAN                                     NOT NULL DEFAULT FALSE,

    description             TEXT,

    /*─────────── Relaciones ───────────*/
    -- Proceso al que pertenece
    process_id              BIGINT                                      NOT NULL
                            REFERENCES processes(id)                    ON DELETE CASCADE,

    -- Tipo de subproceso
    subprocess_type_id      BIGINT                                      NOT NULL
                            REFERENCES subprocess_types(id)             ON DELETE RESTRICT,

    -- Grupo al que pertenece (si aplica)
    group_id                BIGINT                                      NULL
                            REFERENCES subprocess_groups(id)            ON DELETE SET NULL,

    -- Auditoría
    created_at              TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX subprocesses_process_idx          ON subprocesses(process_id);
CREATE INDEX subprocesses_type_idx             ON subprocesses(subprocess_type_id);
CREATE INDEX subprocesses_is_active_idx        ON subprocesses(is_active);

-- Trigger de auditoría: mantiene updated_at en cada UPDATE
CREATE TRIGGER subprocesses_set_updated_at
BEFORE UPDATE ON subprocesses
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- Verificación de tipo de subproceso: debe coincidir con el tipo del grupo si pertenece a uno.
CREATE CONSTRAINT TRIGGER trg_check_group_assignment
AFTER INSERT OR UPDATE ON subprocesses
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION f_subprocess_group_must_match_type();


/*───────────────────────────────────────────────────────────────┐
│ 38. 🖥️   controller_devices                                    │
│ Dispositivos de control (p. ej. ESP32, PLC) instalados en un   │
│ subproceso.                                                    │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE controller_devices (
    id                      BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Información general
    code                    VARCHAR(30)                                 NOT NULL UNIQUE
                            CHECK (
                                code = UPPER(TRIM(code))
                                AND code ~ '^[A-Z0-9_]{1,30}$'
                            ),

    name                    VARCHAR(100)                                NOT NULL
                            CHECK (char_length(TRIM(name)) > 0),

    mac_address             VARCHAR(17)                                 UNIQUE
                            CHECK (
                                mac_address IS NULL
                                OR mac_address ~ '^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
                            ),

    mqtt_topic              VARCHAR(255)                                NOT NULL
                            CHECK (
                                mqtt_topic IS NULL
                                OR char_length(TRIM(mqtt_topic)) > 0
                            ),

    is_active               BOOLEAN                                     NOT NULL DEFAULT TRUE,

    last_seen_at            TIMESTAMPTZ                                 NULL,

    -- Relaciones
    subprocess_id           BIGINT                                      NOT NULL
                            REFERENCES subprocesses(id)                 ON DELETE CASCADE,

    controller_model_id     SMALLINT                                    NULL
                            REFERENCES controller_models(id)            ON DELETE SET NULL,

    -- Auditoría
    created_at              TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX controller_devices_subprocess_idx  ON controller_devices(subprocess_id);
CREATE INDEX controller_devices_is_active_idx   ON controller_devices(is_active);
CREATE INDEX controller_devices_mqtt_topic_idx  ON controller_devices(mqtt_topic);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER controller_devices_set_updated_at
BEFORE UPDATE ON controller_devices
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 39. 📡  sensors                                                │
│ Sensores físicos asociados a un dispositivo de control         │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE sensors (
    id                      BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Información general
    code                    VARCHAR(30)                                 NOT NULL UNIQUE
                            CHECK (
                                code = UPPER(TRIM(code))
                                AND code ~ '^[A-Z0-9_]{1,30}$'
                            ),

    name                    VARCHAR(100)                                NOT NULL
                            CHECK (char_length(TRIM(name)) > 0),

    is_active               BOOLEAN                                     NOT NULL DEFAULT TRUE,
    description             TEXT,

    -- Relaciones
    controller_device_id    BIGINT                                      NOT NULL
                            REFERENCES controller_devices(id)
                            ON DELETE CASCADE,

    sensor_model_id         SMALLINT                                    NULL
                            REFERENCES sensor_models(id)                ON DELETE SET NULL,     -- si el modelo se elimina, el sensor queda sin referencia

    -- Auditoría
    created_at              TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX sensors_controller_device_idx  ON sensors(controller_device_id);
CREATE INDEX sensors_model_idx              ON sensors(sensor_model_id);
CREATE INDEX sensors_is_active_idx          ON sensors(is_active);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER sensors_set_updated_at
BEFORE UPDATE ON sensors
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 40. 🔧 actuators                                               │
│ Actuadores físicos asociados a un dispositivo de control       │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE actuators (
    id                      BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Información general
    code                    VARCHAR(30)                                 NOT NULL UNIQUE
                            CHECK (
                                code = UPPER(TRIM(code))
                                AND code ~ '^[A-Z0-9_]{1,30}$'
                            ),

    name                    VARCHAR(100)                                NOT NULL
                            CHECK (char_length(TRIM(name)) > 0),

    is_active               BOOLEAN                                     NOT NULL DEFAULT TRUE,

    description             TEXT                                        NULL,

    -- Relaciones
    controller_device_id    BIGINT                                      NOT NULL
                            REFERENCES controller_devices(id)           ON DELETE CASCADE,

    actuator_model_id       SMALLINT
                            REFERENCES actuator_models(id)              ON DELETE SET NULL,

    -- Auditoría
    created_at              TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX actuators_controller_device_idx  ON actuators(controller_device_id);
CREATE INDEX actuators_model_idx              ON actuators(actuator_model_id);
CREATE INDEX actuators_is_active_idx          ON actuators(is_active);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER actuators_set_updated_at
BEFORE UPDATE ON actuators
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 41. 🔗 sensor_model_magnitude_links                            │
│ Relación muchos-a-muchos entre modelos de sensores y magnitudes│
└───────────────────────────────────────────────────────────────*/
CREATE TABLE sensor_model_magnitude_links (
    -- Clave compuesta
    sensor_model_id     SMALLINT                                NOT NULL
                        REFERENCES sensor_models(id)
                        ON DELETE CASCADE,

    magnitude_id        SMALLINT                                NOT NULL
                        REFERENCES magnitudes(id)
                        ON DELETE CASCADE,

    -- Auditoría
    created_at          TIMESTAMPTZ                             NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                             NOT NULL DEFAULT now(),

    PRIMARY KEY (sensor_model_id, magnitude_id)
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER sensor_model_magnitude_links_set_updated_at
BEFORE UPDATE ON sensor_model_magnitude_links
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 42. 🔗 actuator_model_magnitude_links                          │
│ Relación muchos-a-muchos entre modelos de actuadores y         │
│ magnitudes                                                     │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE actuator_model_magnitude_links (
    -- Clave compuesta
    actuator_model_id   SMALLINT                                NOT NULL
                        REFERENCES actuator_models(id)
                        ON DELETE CASCADE,

    magnitude_id        SMALLINT                                NOT NULL
                        REFERENCES magnitudes(id)
                        ON DELETE CASCADE,

    -- Auditoría
    created_at          TIMESTAMPTZ                             NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                             NOT NULL DEFAULT now(),

    PRIMARY KEY (actuator_model_id, magnitude_id)
);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER actuator_model_magnitude_links_set_updated_at
BEFORE UPDATE ON actuator_model_magnitude_links
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- ╭──────────────────────────────────────────────────────╮
-- │ ⚙️ 5. Uso y operación                                │
-- ╰──────────────────────────────────────────────────────╯

/*───────────────────────────────────────────────────────────────┐
│ 43. 🤖 bot_users                                               │
│ Usuarios finales que interactúan con los bots a través de      │
│ Telegram.                                                      │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_users (
    -- Identificador único
    id                  BIGINT    GENERATED ALWAYS AS IDENTITY              PRIMARY KEY,

    -- Información de Telegram
    telegram_username   VARCHAR(50)                                         NOT NULL UNIQUE
                        CHECK (char_length(trim(telegram_username)) > 0),

    telegram_user_id    BIGINT                                              NULL UNIQUE,

    -- Estado del usuario
    is_active           BOOLEAN                                             NOT NULL DEFAULT TRUE,

    -- Relaciones
    employee_id         BIGINT                                              NOT NULL UNIQUE
                        REFERENCES employees(id)                            ON DELETE CASCADE,

    -- Auditoría
    created_at        TIMESTAMPTZ   NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ   NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX idx_bot_users_is_active ON bot_users (is_active);

-- Trigger de auditoría: actualiza updated_at en cada UPDATE
CREATE TRIGGER bot_users_set_updated_at
BEFORE UPDATE ON bot_users
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 44. 🔗 bot_user_subscription_links                             │
│ Relación N : M entre bot_users y subscriptions.                │
│ Permite que un mismo usuario de bot se asocie a múltiples      │
│ suscripciones y viceversa.                                     │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_user_subscription_links (
    -- Clave compuesta
    bot_user_id         BIGINT                         NOT NULL
                        REFERENCES bot_users(id)       ON DELETE CASCADE,

    subscription_id     BIGINT                         NOT NULL
                        REFERENCES subscriptions(id)   ON DELETE CASCADE,

    -- Estado del vínculo
    created_at          TIMESTAMPTZ                    NOT NULL DEFAULT now(),

    PRIMARY KEY (bot_user_id, subscription_id)
);

-- Índices auxiliares
CREATE INDEX idx_busl_subscription ON bot_user_subscription_links (subscription_id);

-- Se dispara en cada INSERT/UPDATE sobre la tabla puente
CREATE CONSTRAINT TRIGGER trg_busl_match_company
AFTER INSERT OR UPDATE ON bot_user_subscription_links
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION f_busl_must_match_company();


/*───────────────────────────────────────────────────────────────┐
│ 45. ⚙️ bot_processes                                           │
│ Procesos operativos administrados por un bot dentro de una     │
│ suscripción específica. Cada fila enlaza un proceso de negocio │
│ con la suscripción activa que lo ejecuta.                      │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_processes (
    id                  BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Estado del vínculo
    is_active           BOOLEAN                                     NOT NULL DEFAULT TRUE,

    -- Relaciones
    subscription_id     BIGINT                                      NOT NULL
                        REFERENCES subscriptions(id)                ON DELETE CASCADE,

    process_id          BIGINT                                      NOT NULL
                        REFERENCES processes(id)                    ON DELETE CASCADE,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),

    -- Evita duplicar el mismo proceso en la misma suscripción
    CONSTRAINT uq_bot_processes_subscription_process
        UNIQUE (subscription_id, process_id)
);

-- Índices auxiliares
CREATE INDEX bot_processes_subscription_idx  ON bot_processes(subscription_id);
CREATE INDEX bot_processes_process_idx       ON bot_processes(process_id);
CREATE INDEX bot_processes_is_active_idx     ON bot_processes(is_active);

-- Trigger de auditoría: mantiene updated_at en cada UPDATE
CREATE TRIGGER bot_processes_set_updated_at
BEFORE UPDATE ON bot_processes
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 46. 👤 user_processes                                          │
│ Procesos asignados a un usuario de bot. Cada vínculo indica    │
│ qué procesos de negocio puede operar (o vigilar) un usuario    │
│ determinado dentro de la plataforma.                           │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE user_processes (
    id                  BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Estado del vínculo
    is_active           BOOLEAN                                     NOT NULL DEFAULT TRUE,

    -- Relaciones
    bot_user_id         BIGINT                                      NOT NULL
                        REFERENCES bot_users(id)
                        ON DELETE CASCADE,

    process_id          BIGINT                                      NOT NULL
                        REFERENCES processes(id)
                        ON DELETE CASCADE,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),

    -- Evita que un mismo proceso se asigne dos veces al mismo usuario
    CONSTRAINT uq_user_processes_user_process
        UNIQUE (bot_user_id, process_id)
);

-- Índices auxiliares
CREATE INDEX user_processes_user_idx       ON user_processes(bot_user_id);
CREATE INDEX user_processes_process_idx    ON user_processes(process_id);
CREATE INDEX user_processes_is_active_idx  ON user_processes(is_active);

-- Trigger de auditoría: mantiene updated_at en cada UPDATE
CREATE TRIGGER user_processes_set_updated_at
BEFORE UPDATE ON user_processes
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- ╭──────────────────────────────────────────────────────╮
-- │ 💰 6. Facturación y pagos                            │
-- ╰──────────────────────────────────────────────────────╯

/*───────────────────────────────────────────────────────────────┐
│ 47. 📅 subscription_periods                                    │
│ Periodos de facturación pertenecientes a una suscripción.      │
│ Cada fila resume el plan en vigor durante ese intervalo, así   │
│ como su snapshot comercial para histórico de precios y límites.│
└───────────────────────────────────────────────────────────────*/
CREATE TABLE subscription_periods (
    id                  BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Relación con la suscripción
    subscription_id     BIGINT                                      NOT NULL
                        REFERENCES subscriptions(id)
                        ON DELETE CASCADE,

    -- Intervalo de facturación
    period_start        TIMESTAMPTZ                                 NOT NULL,
    period_end          TIMESTAMPTZ                                 NOT NULL
                        CHECK (period_end > period_start),

    -- Snapshot del plan en el momento del periodo
    plan_snapshot       JSONB                                       NOT NULL,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX subscription_periods_subscription_idx ON subscription_periods(subscription_id);

-- Trigger de auditoría: mantiene updated_at en cada UPDATE
CREATE TRIGGER subscription_periods_set_updated_at
BEFORE UPDATE ON subscription_periods
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 48. 🧾 invoices                                                │
│ Facturas emitidas para cada periodo de suscripción.            │
│ Contiene montos, fechas clave y estado de cobranza.            │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE invoices (
    id                      BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Relación con el periodo facturado
    subscription_period_id  BIGINT                                      NOT NULL UNIQUE
                            REFERENCES subscription_periods(id)         ON DELETE CASCADE,

    -- Identificación y monto
    invoice_number          VARCHAR(50)                                 NOT NULL UNIQUE
                            CHECK (
                                char_length(TRIM(invoice_number)) > 0
                            ),

    amount_due              NUMERIC(10, 2)                              NOT NULL
                            CHECK (amount_due >= 0),

    currency                CHAR(3)                                     NOT NULL DEFAULT 'COP'
                            CHECK (currency ~ '^[A-Z]{3}$'),

    -- Fechas clave
    issued_at               TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    due_date                TIMESTAMPTZ                                 NOT NULL
                            CHECK (due_date >= issued_at),

    -- Estado de la factura
    invoice_status_id       SMALLINT
                            REFERENCES invoice_statuses(id)             ON DELETE RESTRICT,

    -- Auditoría
    created_at              TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX invoices_status_idx               ON invoices(invoice_status_id);
CREATE INDEX invoices_due_date_idx             ON invoices(due_date);

-- Trigger de auditoría: mantiene updated_at en cada UPDATE
CREATE TRIGGER invoices_set_updated_at
BEFORE UPDATE ON invoices
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 49. 💳 payments                                                │
│ Pagos registrados para saldar facturas                         │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE payments (
    id                          BIGINT    GENERATED ALWAYS AS IDENTITY      PRIMARY KEY,

    -- Relación con la factura
    invoice_id                  BIGINT                                      NOT NULL
                                REFERENCES invoices(id)                     ON DELETE CASCADE,

    -- Información del pago
    amount                      NUMERIC(10, 2)                              NOT NULL
                                CHECK (amount >= 0),

    currency                    CHAR(3)                                     NOT NULL DEFAULT 'COP'
                                CHECK (currency ~ '^[A-Z]{3}$'),

    paid_at                     TIMESTAMPTZ                                 NOT NULL DEFAULT now(),

    provider_transaction_id     VARCHAR(100)                                NOT NULL UNIQUE
                                CHECK (char_length(TRIM(provider_transaction_id)) > 0),

    payment_method_id           SMALLINT                                    NOT NULL
                                REFERENCES payment_methods(id)              ON DELETE RESTRICT,          -- si se elimina el método, se conserva el pago

    -- Auditoría
    created_at                  TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at                  TIMESTAMPTZ                                 NOT NULL DEFAULT now()
);

-- Índices auxiliares
CREATE INDEX payments_invoice_idx          ON payments(invoice_id);
CREATE INDEX payments_payment_method_idx   ON payments(payment_method_id);
CREATE INDEX payments_provider_transaction_idx ON payments(provider_transaction_id);

-- Trigger de auditoría: mantiene updated_at en cada UPDATE
CREATE TRIGGER payments_set_updated_at
BEFORE UPDATE ON payments
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 50. 🔁 payment_attempts                                        │
│ Registro de cada intento de pago asociado a una factura.       │
│ Permite rastrear reintentos automáticos o manuales, su estado  │
│ y el método utilizado.                                         │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE payment_attempts (
    id                      BIGINT    GENERATED ALWAYS AS IDENTITY  PRIMARY KEY,

    -- Relación con la factura
    invoice_id              BIGINT                                  NOT NULL
                            REFERENCES invoices(id)
                            ON DELETE CASCADE,

    -- Nº de intento (1, 2, 3…)
    attempt_no              SMALLINT                                NOT NULL
                            CHECK (attempt_no >= 1),

    -- Mensaje devuelto por el procesador o descripción
    message                 TEXT                                    NOT NULL,

    response_code           VARCHAR(50)                             NOT NULL
                            CHECK (
                                char_length(
                                    TRIM(response_code)
                                ) > 0
                            ),

    is_final                BOOLEAN                                 NOT NULL DEFAULT FALSE,

    attempted_at            TIMESTAMPTZ                             NOT NULL DEFAULT now(),

    payment_method_id       SMALLINT
                            REFERENCES payment_methods(id)          ON DELETE RESTRICT,

    payment_status_id       SMALLINT
                            REFERENCES payment_statuses(id)         ON DELETE RESTRICT,

    -- Auditoría
    created_at              TIMESTAMPTZ                             NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ                             NOT NULL DEFAULT now(),

    -- Evita duplicar el mismo Nº de intento en la misma factura
    UNIQUE (invoice_id, attempt_no)
);

-- Índices auxiliares
CREATE INDEX payment_attempts_invoice_idx        ON payment_attempts(invoice_id);
CREATE INDEX payment_attempts_status_idx         ON payment_attempts(payment_status_id);
CREATE INDEX payment_attempts_method_idx         ON payment_attempts(payment_method_id);

-- Trigger de auditoría: mantiene updated_at en cada UPDATE
CREATE TRIGGER payment_attempts_set_updated_at
BEFORE UPDATE ON payment_attempts
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- ╭──────────────────────────────────────────────────────╮
-- │ 🛡️ 6. Permisos                                       │
-- ╰──────────────────────────────────────────────────────╯

/*───────────────────────────────────────────────────────────────┐
│ 51. 🔗 bot_process_permission_links                            │
│ Permisos que un bot posee sobre un proceso concreto.           │
│ Tabla puente muchos-a-muchos entre bot_processes y             │
│ bot_process_permissions.                                       │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE bot_process_permission_links (
    -- Clave compuesta
    bot_process_id      BIGINT                                  NOT NULL
                        REFERENCES bot_processes(id)            ON DELETE CASCADE,

    permission_id       SMALLINT                                NOT NULL
                        REFERENCES bot_process_permissions(id)  ON DELETE CASCADE,

    -- Auditoría
    created_at          TIMESTAMPTZ                             NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                             NOT NULL DEFAULT now(),

    PRIMARY KEY (bot_process_id, permission_id)
);

-- Trigger de auditoría: mantiene updated_at en cada UPDATE
CREATE TRIGGER bot_process_permission_links_set_updated_at
BEFORE UPDATE ON bot_process_permission_links
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


/*───────────────────────────────────────────────────────────────┐
│ 52. 🔗 user_process_permission_links                           │
│ Permisos que un usuario de bot posee sobre un proceso concreto │
│ (relación muchos-a-muchos).                                    │
└───────────────────────────────────────────────────────────────*/
CREATE TABLE user_process_permission_links (
    -- Clave compuesta
    user_process_id     BIGINT                                      NOT NULL
                        REFERENCES user_processes(id)               ON DELETE CASCADE,

    permission_id       SMALLINT                                    NOT NULL
                        REFERENCES user_process_permissions(id)     ON DELETE CASCADE,

    -- Auditoría
    created_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ                                 NOT NULL DEFAULT now(),

    PRIMARY KEY (user_process_id, permission_id)
);

-- Trigger de auditoría: mantiene updated_at en cada UPDATE
CREATE TRIGGER user_process_permission_links_set_updated_at
BEFORE UPDATE ON user_process_permission_links
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();
