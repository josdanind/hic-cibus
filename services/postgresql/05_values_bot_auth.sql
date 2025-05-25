\c bot_auth_db;

INSERT INTO bot_access_roles (name, description) VALUES
    ('viewer',   'Permiso de solo lectura: puede ver datos pero no modificarlos'),
    ('editor',   'Permiso de edición: puede crear y actualizar recursos, pero no borrar ni gestionar roles'),
    ('admin',    'Permiso de administrador: puede crear, editar y borrar recursos, pero no asignar roles'),
    ('owner',    'Propietario: control total, incluye gestión de roles y permisos de otros usuarios'),
    ('operator', 'Operador: puede ejecutar acciones operativas específicas, sin acceso administrativo');

INSERT INTO roles (name, description) VALUES
    ('Responsable legal',           'Encargado de la gestión jurídica y cumplimiento normativo'),
    ('Responsable de ventas',       'Coordina y supervisa el equipo de ventas'),
    ('Responsable de soporte técnico','Atiende y resuelve incidencias técnicas de clientes internos y externos'),
    ('Administrador de sistemas',   'Gestiona la infraestructura y la seguridad de los sistemas TI'),
    ('Analista de datos',           'Realiza análisis, reportes e interpretación de datos empresariales');

INSERT INTO payment_statuses (name, description) VALUES
    ('pending',   'Pago pendiente de procesamiento'),
    ('completed', 'Pago completado con éxito'),
    ('failed',    'Pago fallido debido a un error en la transacción'),
    ('canceled',  'Pago cancelado por el usuario o el sistema'),
    ('refunded',  'Pago reembolsado al cliente');

INSERT INTO subscription_statuses (name, description) VALUES
    ('activa',     'Suscripción vigente y en uso'),
    ('suspendida', 'Suscripción temporalmente deshabilitada'),
    ('cancelada',  'Suscripción terminada y no renovada');

INSERT INTO subscription_periods (name, description) VALUES
    ('mensual',    'Facturación cada mes'),
    ('trimestral', 'Facturación cada tres meses'),
    ('anual',      'Facturación cada año');

INSERT INTO bot_environments (name, description) VALUES
    ('producción', 'Entorno estable donde los bots sirven a usuarios finales'),
    ('desarrollo', 'Entorno para pruebas y depuración de nuevas funcionalidades'),
    ('staging',    'Entorno intermedio que replica producción para validaciones finales'),
    ('qa',         'Entorno de pruebas de calidad automatizadas y manuales');


INSERT INTO bot_statuses (name, description) VALUES
    ('operativo',         'Bot funcionando correctamente y atendiendo solicitudes'),
    ('en mantenimiento',  'Bot detenido temporalmente para tareas de mantenimiento'),
    ('apagado',           'Bot inactivo y sin servicio'),
    ('en espera',         'Bot aguardando activación o nuevos trabajos'),
    ('error',             'Bot con fallo crítico que requiere intervención');

INSERT INTO bot_model_statuses (name, description) VALUES
    ('en desarrollo', 'El modelo está en fase de desarrollo y pruebas'),
    ('en producción', 'El versión estable del modelo desplegada en producción'),
    ('obsoleto',      'El modelo ha sido reemplazado por versiones más recientes'),
    ('beta',          'El modelo está en versión beta para pruebas limitadas'),
    ('deprecated',    'El modelo sigue disponible pero no se recomienda su uso');

INSERT INTO bot_models (name, description, version, status_id) VALUES
    ('Tlaloc V1.0',  'Modelo inicial de Tlaloc para monitorización de cultivos', 'v1.0', 1);

INSERT INTO bot_categories (name, description) VALUES
    ('monitoreo',   'Bots orientados a la supervisión y recolección de datos en tiempo real'),
    ('agricultura', 'Bots para gestión y monitoreo de cultivos y entornos agrícolas'),
    ('análisis',    'Bots que procesan datos y generan reportes analíticos');
