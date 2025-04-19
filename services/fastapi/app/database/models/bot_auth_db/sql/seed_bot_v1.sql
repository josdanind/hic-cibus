-- 1. Estados de Modelos
INSERT INTO bot_model_statuses (id, name, description) VALUES
(1, 'Activo', 'Modelo en uso activo'),
(2, 'En desarrollo', 'Modelo en fase de desarrollo');

-- 2. Modelos de Bot
INSERT INTO bot_models (id, name, description, version, status_id, created_at, updated_at) VALUES
(1, 'Tlaloc V1.0', 'Modelo inicial para monitoreo de cultivos', '1.0', 1, NOW(), NOW()),
(2, 'Quetzalcoatl V2.0', 'Modelo experimental de análisis de datos agrícolas', '2.0', NULL, NOW(), NOW());

-- 3. Estados de Bots
INSERT INTO bot_statuses (id, name, description) VALUES
(1, 'Operativo', 'Bot en funcionamiento'),
(2, 'En mantenimiento', 'Bot en revisión técnica');

-- 4. Entornos de Bots
INSERT INTO bot_environments (id, name, description) VALUES
(1, 'Producción', 'Entorno productivo'),
(2, 'Desarrollo', 'Entorno de pruebas y desarrollo');

-- 5. Categorías
INSERT INTO bot_categories (id, name, description, created_at, updated_at) VALUES
(1, 'Agricultura', 'Bots relacionados con agricultura', NOW(), NOW()),
(2, 'Finanzas', 'Bots relacionados con análisis financiero', NOW(), NOW()),
(3, 'Análisis de Datos', 'Bots orientados al análisis de datos', NOW(), NOW());

-- 6. Bots
INSERT INTO bots (
    id, name, description, api_url, is_active, last_ping, request_per_minute, data,
    bot_model_id, status_id, environment_id, created_at, updated_at
) VALUES
-- Bot 1: TlalocBot
(1, 'TlalocBot', 'Bot que monitorea condiciones del cultivo', 'https://api.tlaloc.local/bot',
TRUE, NOW(), 15, '{"sensor": "activo"}', 1, 1, 1, NOW(), NOW()),
-- Bot 2: QuetzalcoatlBot
(2, 'QuetzalcoatlBot', 'Bot que analiza datos de sensores en fase experimental', 'https://api.quetzal.local/bot',
FALSE, NOW(), 30, '{"sensor": "inactivo", "modo": "debug"}', 2, 2, 2, NOW(), NOW());

-- 7. Relación Bot-Categoría
INSERT INTO bot_category_link (bot_id, category_id) VALUES
(1, 1),  -- TlalocBot → Agricultura
(2, 2),  -- QuetzalcoatlBot → Finanzas
(2, 3);  -- QuetzalcoatlBot → Análisis de Datos

-- 8. Credenciales de los Bots
INSERT INTO bot_credentials (
    id, hashed_password, hashed_telegram_bot_token, hashed_api_access_token,
    bot_id, created_at, updated_at
) VALUES
(1, 'hash123', 'telegramtokenhash', 'apitokenhash', 1, NOW(), NOW()),
(2, 'hash456', 'telegramtokenhash2', 'apitokenhash2', 2, NOW(), NOW()),
-- Credencial sin bot asignado
(3, 'hash789', 'telegramtokenhash3', 'apitokenhash3', NULL, NOW(), NOW());