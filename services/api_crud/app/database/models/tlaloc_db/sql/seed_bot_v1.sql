-- 'roles'
INSERT INTO roles (name, description) VALUES
('Responsable legal', 'Encargado de representar legalmente a la empresa.'),
('Responsable de ventas', 'Gestiona y supervisa las actividades comerciales de la empresa.'),
('Responsable de soporte técnico', 'Proporciona soporte y asistencia técnica a los clientes y usuarios internos.'),
('Operario de huertas', 'Responsable de labores operativas en las huertas, incluyendo siembra, mantenimiento y cosecha.');


-- 'companies'
INSERT INTO companies (
    name, description, is_active, phone, email, website, country, city, state, zip_code, address
) VALUES
(
    'AgroTech SAS',
    'Empresa dedicada a la implementación de soluciones tecnológicas en agricultura.',
    true,
    '+571234567890',
    'info@agrotech.com',
    'https://agrotech.com',
    'Colombia',
    'Bogotá',
    'Cundinamarca',
    '110111',
    'Calle 123 #45-67'
),
(
    'Huertas del Llano',
    'Producción y comercialización de frutas y verduras orgánicas.',
    true,
    '+578765432109',
    'contacto@huertasdelllano.com',
    'https://huertasdelllano.com',
    'Colombia',
    'Villavicencio',
    'Meta',
    '500001',
    'Km 15 vía Restrepo'
);


-- 'employees'
INSERT INTO employees (
    first_name, middle_name, last_name, second_last_name, mobile_phone, email, position, role_id, company_id
) VALUES
('Carlos', 'Andrés', 'Gómez', 'Rincón', '+573001112233', 'carlos.gomez@example.com', 'Gerente General', 1, 1),
('Laura', NULL, 'Martínez', 'Díaz', '+573002223344', 'laura.martinez@example.com', 'Ejecutiva de Ventas', 2, 1),
('Pedro', 'José', 'Quintero', NULL, '+573003334455', 'pedro.quintero@example.com', 'Técnico de Soporte', 3, 1),
('Ana', 'María', 'Castro', 'López', '+573004445566', 'ana.castro@example.com', 'Operaria Agrícola', 4, 2);


-- 'company_contacts'
INSERT INTO company_contacts (
    is_primary, notes, employee_id
) VALUES
(true, 'Contacto principal para asuntos administrativos y legales.', 1),
(true, 'Contacto principal para temas operativos y agrícolas.', 4),
(false, 'Contacto secundario para soporte técnico y consultas técnicas.', 3);


-- `bot_user_permissions`
INSERT INTO bot_user_permissions (
    name, description
) VALUES
('viewer', 'Permiso de solo lectura, puede visualizar información sin modificarla.'),
('editor', 'Permiso para modificar y actualizar información básica.'),
('admin', 'Permiso administrativo con control completo sobre el bot y sus configuraciones.'),
('owner', 'Propietario del bot, con capacidad total incluyendo la gestión de permisos de otros usuarios.');


-- 'bot_user'
INSERT INTO bot_users (
    telegram_username, telegram_user_id, is_active, employee_id, permissions_id
) VALUES
('carlosgomez', 123456789, true, 1, 4),  -- Owner
('lauram', 987654321, true, 2, 2),       -- Editor
('pedrotech', 555666777, true, 3, 3),    -- Admin
('anacastro', 444333222, true, 4, 1);    -- Viewer


-- 'bot_category'
INSERT INTO bot_categories (
    name, description
) VALUES
(
    'monitoreo',
    'Bots especializados en recopilar datos ambientales y agronómicos para su análisis.'
),
(
    'análisis',
    'Bots enfocados en procesar y analizar información histórica o en tiempo real.'
),
(
    'control',
    'Bots que ejecutan acciones automáticas como riego, ventilación o iluminación.'
),
(
    'soporte técnico',
    'Bots utilizados para brindar asistencia técnica a usuarios de plataformas.'
);


-- 'bot_model_statuses'
INSERT INTO bot_model_statuses (
    name, description
) VALUES
('en desarrollo', 'Modelo en construcción, aún no desplegado en entornos productivos.'),
('producción', 'Modelo final y activo en entornos de producción.'),
('obsoleto', 'Modelo antiguo que ya no se utiliza o fue reemplazado.');

-- 'bot_models'
INSERT INTO bot_models (
    name, description, version, status_id
) VALUES
(
    'Tlaloc V1.0',
    'Modelo inicial para monitoreo y control de cultivos mediante sensores.',
    '1.0',
    2  -- producción
),
(
    'Quetzalcoatl V2.1',
    'Modelo experimental enfocado en análisis predictivo para agricultura.',
    '2.1',
    1  -- en desarrollo
),
(
    'IntiBot V0.9',
    'Versión preliminar para pruebas con integración de clima y suelos.',
    '0.9',
    3  -- obsoleto
);


-- 'bot_statuses'
INSERT INTO bot_statuses (
    name, description
) VALUES
('operativo', 'Bot funcionando correctamente y disponible para los usuarios.'),
('en mantenimiento', 'Bot temporalmente fuera de servicio por ajustes o mejoras.'),
('apagado', 'Bot detenido manualmente o por errores críticos.'),
('en espera', 'Bot en estado inactivo hasta su activación.');


-- 'bot_environments'
INSERT INTO bot_environments (
    name, description
) VALUES
('producción', 'Entorno activo en el que los bots interactúan con usuarios reales.'),
('desarrollo', 'Entorno de pruebas y ajustes antes de pasar a producción.'),
('testing', 'Entorno aislado para pruebas automatizadas o QA.'),
('staging', 'Entorno espejo de producción para pruebas finales previas al despliegue.');


-- 'bot'
INSERT INTO bots (
    name, description, api_url, is_active, last_ping, request_per_minute, data,
    bot_model_id, status_id, environment_id
) VALUES
(
    'Tlaloc',
    'Bot de monitoreo de humedad y temperatura en parcelas agrícolas.',
    'https://api.tlaloc.hic-cibus.com',
    true,
    NOW(),
    60,
    '{"tipo":"sensor","funciones":["riego automático","alertas"]}',
    1,  -- Tlaloc V1.0
    1,  -- operativo
    1   -- producción
),
(
    'Quetzalcoatl',
    'Bot de análisis de datos históricos y predicción climática.',
    'https://api.quetzalcoatl.hic-cibus.com',
    false,
    NULL,
    100,
    '{"modulo":"IA","estado":"experimental"}',
    2,  -- Quetzalcoatl V2.1
    2,  -- en mantenimiento
    2   -- desarrollo
),
(
    'IntiBot',
    'Bot obsoleto para pruebas de integración inicial.',
    'https://api.intibot.hic-cibus.com',
    false,
    NULL,
    20,
    '{"estado":"retirado"}',
    3,  -- IntiBot V0.9
    3,  -- apagado
    3   -- testing
);


-- 'bot_credentials'
INSERT INTO bot_credentials (
    hashed_password, hashed_telegram_bot_token, hashed_api_access_token, bot_id
) VALUES
(
    '$2b$12$abcdef1234567890hashedpassword1',
    '$2b$12$telegramtokenhashed123abc',
    '$2b$12$apiactokenhashed456def',
    1  -- Tlaloc
),
(
    '$2b$12$abcdef1234567890hashedpassword2',
    '$2b$12$telegramtokenhashed789xyz',
    NULL,
    2  -- Quetzalcoatl
),
(
    '$2b$12$abcdef1234567890hashedpassword3',
    NULL,
    NULL,
    3  -- IntiBot
);


-- 'bot_user_link'
INSERT INTO user_bot_link (
    user_id, bot_id, can_access, granted_at, revoked_at
) VALUES
(
    1, 1, true, NOW(), NULL  -- Carlos → Tlaloc (acceso activo)
),
(
    2, 1, true, NOW(), NULL  -- Laura → Tlaloc (acceso activo)
),
(
    3, 2, true, '2025-03-01 08:00:00', '2025-04-01 08:00:00'  -- Pedro → Quetzalcoatl (acceso revocado)
),
(
    4, 3, true, NOW(), NULL  -- Ana → IntiBot (acceso activo)
);


-- 'bot_category_link'
INSERT INTO bot_category_link (bot_id, category_id) VALUES
(1, 1),  -- Tlaloc → monitoreo
(1, 3),  -- Tlaloc → control
(2, 2),  -- Quetzalcoatl → análisis
(3, 1),  -- IntiBot → monitoreo
(3, 4);  -- IntiBot → soporte técnico


-- 'subscription_statuses'
INSERT INTO subscription_statuses (name, description) VALUES
('activa', 'Suscripción actualmente en uso y con pagos al día.'),
('suspendida', 'La suscripción está pausada temporalmente.'),
('cancelada', 'La suscripción fue terminada permanentemente.');


-- 'subscription_periods'
INSERT INTO subscription_periods (name, description) VALUES
('mensual', 'La facturación se realiza cada mes.'),
('trimestral', 'La facturación se realiza cada tres meses.'),
('anual', 'La facturación se realiza una vez al año.');


-- 'payment_statuses'
INSERT INTO payment_statuses (name, description) VALUES
('pendiente', 'El pago está registrado pero aún no se ha completado.'),
('completado', 'El pago fue realizado y confirmado exitosamente.'),
('fallido', 'El intento de pago no fue exitoso.'),
('cancelado', 'El pago fue anulado antes de su procesamiento.');


-- 'subscriptions'
INSERT INTO subscriptions (
    is_active, max_users, start_date, end_date, next_payment_date, last_payment_date,
    notes, bot_id, company_id, status_id, subscription_period_id
) VALUES
(
    true, 5, '2025-01-01', NULL, '2025-05-01', '2025-04-01',
    'Suscripción principal de monitoreo.', 1, 1, 1, 1
),
(
    false, 10, '2024-06-01', '2025-06-01', NULL, '2025-03-15',
    'Cliente suspendido por falta de pago.', 2, 2, 2, 3
);


-- subscription_payments
INSERT INTO subscription_payments (
    amount, payment_date, payment_method, transaction_id, payment_status_id, subscription_id
) VALUES
(
    50000.0, '2025-04-01', 'PSE', 'TXN1234567890', 2, 1
),
(
    150000.0, NULL, 'Tarjeta crédito', 'TXN9876543210', 1, 2
);
