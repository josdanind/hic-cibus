-- mqtt_user_core_models_v0.1.0.sql
-- ==========================================
-- 💾 CODE: MQTT_USER_CORE_MODELS
-- 📌 VERSIÓN: v0.1.0
-- 📦 DESCRIPCIÓN:
--      Modelos base del núcleo de datos de
--      para el manejo de usuarios MQTT
-- 📅 FECHA: 2025-09-10
-- ==========================================

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