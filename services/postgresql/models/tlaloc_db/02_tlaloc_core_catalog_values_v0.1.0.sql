-- tlaloc_core_catalog_values_v0.1.0.sql
-- ==========================================
-- 💾 CODE: TLALOC_CORE_CATALOG_VALUES
-- 📌 VERSIÓN: v0.1.0
-- 📦 DESCRIPCIÓN:
--      Valores de catálogos base del núcleo de datos de
--      Tlaloc
-- 🧠 LÓGICA:
--      - tlaloc_core_models_v0.2.0.sql
-- 📅 FECHA: 2025-09-10
-- ==========================================

-- Estados del bot
INSERT INTO bot_statuses (code, name, description)
VALUES
    ('ONLINE',      'En línea',       'El bot está en línea y operativo'),
    ('OFFLINE',     'Fuera de línea', 'El bot no está disponible actualmente'),
    ('ERROR',       'Con error',      'El bot ha encontrado un error crítico'),
    ('MAINTENANCE', 'Mantenimiento',  'El bot está en mantenimiento programado'),
    ('BOOTING',     'Arrancando',     'El bot se está iniciando y aún no está disponible'),
    ('RESTARTING',  'Reiniciando',    'El bot está reiniciando su servicio'),
    ('DEGRADED',    'Degradado',      'El bot está funcionando con capacidad limitada'),
    ('DISABLED',    'Deshabilitado',  'El bot fue desactivado manualmente por un administrador');

-- Entornos disponibles del bot
INSERT INTO bot_environments (code, name, description)
VALUES
    ('PRODUCTION',  'Producción',   'Entorno real de operación del bot'),
    ('DEVELOPMENT', 'Desarrollo',   'Entorno para pruebas y desarrollo de nuevas funcionalidades'),
    ('TESTING',     'Pruebas',      'Entorno intermedio para validación previa a producción'),
    ('STAGING',     'Staging',      'Réplicas casi exactas del entorno de producción para validación final'),
    ('SANDBOX',     'Sandbox',      'Entorno seguro y aislado para experimentación');

-- Estados del modelo del bot
INSERT INTO bot_model_statuses (code, name, description)
VALUES
    ('DRAFT',         'Borrador',        'El modelo está en estado inicial y aún no se ha validado'),
    ('TESTING',       'En pruebas',      'El modelo está siendo probado antes de su liberación'),
    ('READY',         'Listo',           'El modelo está listo para ser implementado'),
    ('PRODUCTION',    'En producción',   'El modelo está actualmente en uso en un entorno productivo'),
    ('DEPRECATED',    'Obsoleto',        'El modelo ya no se recomienda para su uso'),
    ('ARCHIVED',      'Archivado',       'El modelo fue archivado y está fuera de uso activo');

-- Categorías del bot
INSERT INTO bot_categories (code, name, description)
VALUES
    ('MONITORING',        'Monitoreo',            'Bots dedicados a supervisar variables o eventos del sistema'),
    ('AUTOMATION',        'Automatización',       'Bots que ejecutan tareas sin intervención humana'),
    ('NOTIFICATIONS',     'Notificaciones',       'Bots que envían alertas o mensajes informativos'),
    ('ASSISTANT',         'Asistente',            'Bots que interactúan directamente con usuarios finales'),
    ('REPORTING',         'Reportes',             'Bots que generan y entregan informes automáticos'),
    ('CONTROL',           'Control',              'Bots que ejecutan órdenes para actuar sobre dispositivos o procesos'),
    ('SMART_FARMING',     'Agricultura inteligente','Bots diseñados para monitorear y controlar cultivos mediante sensores y actuadores en contextos de agricultura de precisión'),
    ('TRADING',           'Trading',              'Bots especializados en operaciones de compra y venta en mercados financieros o de criptomonedas');

-- Permisos para procesos de bots
INSERT INTO bot_process_permissions (code, name, description)
VALUES
    ('CREATE',      'Crear',            'Permite crear nuevos procesos'),
    ('READ',        'Leer',             'Permite leer información de procesos existentes'),
    ('UPDATE',      'Actualizar',       'Permite modificar procesos existentes'),
    ('DELETE',      'Eliminar',         'Permite eliminar procesos existentes'),
    ('ADMIN',       'Administrar',      'Permite administrar todos los aspectos de los procesos'),
    ('CONFIGURE',   'Configurar',       'Permite configurar parámetros y ajustes de procesos'),
    ('VIEW_LOGS',   'Ver registros',    'Permite ver los registros de actividad de los procesos'),
    ('EXECUTE',     'Ejecutar',         'Permite ejecutar procesos definidos');

-- Permisos de procesos de bots
INSERT INTO user_process_permissions (code, name, description)
VALUES
    ('VIEW', 'Visualizar', 'Permite ver información del proceso pero no modificarla.'),
    ('EDIT', 'Editar', 'Permite modificar configuraciones o información del proceso.'),
    ('CONTROL', 'Controlar', 'Permite enviar comandos a actuadores del proceso.'),
    ('AUDIT', 'Auditoría', 'Permite ver historial de eventos, cambios y registros.');

-- Unidades de período
INSERT INTO period_units (code, name_es, description)
VALUES
    ('DAILY',     'Diario',       'Período de un día'),
    ('WEEKLY',    'Semanal',      'Período de siete días consecutivos'),
    ('BIWEEKLY',  'Quincenal',    'Período de catorce días'),
    ('MONTHLY',   'Mensual',      'Período de un mes'),
    ('BIMONTHLY', 'Bimestral',    'Período de dos meses'),
    ('QUARTERLY', 'Trimestral',   'Período de tres meses'),
    ('SEMIANNUAL','Semestral',    'Período de seis meses'),
    ('ANNUAL',    'Anual',        'Período de doce meses');

-- Estados de suscripción
INSERT INTO subscription_statuses (code, name, description)
VALUES
    ('ACTIVE',         'Activa',              'La suscripción está en curso y habilitada para operar'),
    ('GRACE_PERIOD',   'Período de gracia',   'La suscripción ha vencido pero tiene un margen de tiempo antes de ser cancelada'),
    ('SUSPENDED',      'Suspendida',          'La suscripción está temporalmente inactiva por problemas de pago u otros motivos'),
    ('CANCELLED',      'Cancelada',           'La suscripción fue cancelada manualmente o por el sistema'),
    ('EXPIRED',        'Expirada',            'La suscripción alcanzó su fecha de finalización sin renovación'),
    ('PENDING',        'Pendiente',           'La suscripción fue creada pero aún no ha sido activada');

-- Estados de facturas
INSERT INTO invoice_statuses (code, name, description)
VALUES
    ('PENDING',         'Pendiente',            'La factura fue generada pero aún no ha sido pagada.'),
    ('PARTIALLY_PAID',  'Parcialmente Pagada',  'La factura ha sido pagada parcialmente, pero aún tiene un saldo pendiente.'),
    ('PAID',            'Pagada',               'La factura ha sido pagada correctamente.'),
    ('FAILED',          'Fallida',              'El intento de pago de la factura falló.'),
    ('EXPIRED',         'Expirada',             'La factura superó su fecha de vencimiento sin ser pagada.'),
    ('CANCELLED',       'Cancelada',            'La factura fue cancelada manualmente o por el sistema.');


-- Métodos de pago disponibles
INSERT INTO payment_methods (code, name, description)
VALUES
    ('CREDIT_CARD',   'Tarjeta de Crédito',        'Pago con tarjeta de crédito a través de una pasarela.'),
    ('DEBIT_CARD',    'Tarjeta Débito',            'Pago con tarjeta débito mediante autenticación bancaria.'),
    ('PSE',           'PSE / Transferencia',       'Pago con débito a cuenta bancaria usando PSE.'),
    ('NEQUI',         'Nequi',                     'Pago usando la billetera digital Nequi.'),
    ('DAVIPLATA',     'Daviplata',                 'Pago a través de la billetera móvil Daviplata.'),
    ('EFECTY',        'Efecty',                    'Pago en efectivo en puntos Efecty.'),
    ('BITCOIN',       'Bitcoin',                   'Pago con criptomoneda Bitcoin (BTC) a través de red blockchain.'),
    ('CARDANO',       'Cardano (ADA)',             'Pago con criptomoneda Cardano (ADA) usando dirección propia.'),
    ('TON',           'TON (The Open Network)',    'Pago con TON, criptomoneda integrada con Telegram y TON blockchain.'),
    ('INTERNAL',      'Crédito interno / Wallet',  'Pago con saldo interno disponible en la plataforma.');


-- Estados de los intentos de pago
INSERT INTO payment_statuses (code, name, description)
VALUES
    ('PENDING',        'Pendiente',            'El intento de pago fue iniciado pero aún no ha sido confirmado.'),
    ('PROCESSING',     'Procesando',           'El pago está en curso y aún no se ha recibido respuesta del proveedor.'),
    ('SUCCESS',        'Exitoso',              'El pago fue completado y confirmado con éxito.'),
    ('FAILED',         'Fallido',              'El intento de pago falló por error en el proceso.'),
    ('DECLINED',       'Rechazado',            'El proveedor de pagos rechazó el intento (fondos insuficientes, tarjeta bloqueada, etc.).'),
    ('EXPIRED',        'Expirado',             'El intento de pago no fue completado dentro del tiempo límite.'),
    ('CANCELLED',      'Cancelado',            'El intento fue cancelado por el usuario o el sistema.');

