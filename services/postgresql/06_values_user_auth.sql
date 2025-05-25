\c user_auth_db;

INSERT INTO access_roles (name, description) VALUES
    ('viewer',   'Permiso de solo lectura: puede ver datos pero no modificarlos'),
    ('editor',   'Permiso de edición: puede crear y actualizar recursos, pero no borrar ni gestionar roles'),
    ('admin',    'Permiso de administrador: puede crear, editar y borrar recursos, pero no asignar roles'),
    ('owner',    'Propietario: control total, incluye gestión de roles y permisos de otros usuarios'),
    ('operator', 'Operador: puede ejecutar acciones operativas específicas, sin acceso administrativo');

INSERT INTO job_positions (name, description) VALUES
    ('Gerente de proyecto', 'Supervisa la planificación, ejecución y cierre de proyectos'),
    ('Analista de datos', 'Recopila y analiza datos para apoyar la toma de decisiones'),
    ('Responsable de ventas', 'Encargado de gestionar el equipo y estrategias de ventas'),
    ('Ingeniero de software', 'Desarrolla y mantiene aplicaciones y sistemas internos'),
    ('Agrónomo', 'Especialista en agronomía y manejo de cultivos para optimizar la producción agrícola'),
    ('Coordinador de marketing', 'Diseña y coordina campañas de marketing y comunicación'),
    ('Ingeniero electrónico', 'Diseña y desarrolla sistemas electrónicos y dispositivos'),
    ('Ingeniero mecánico', 'Diseña y mantiene sistemas mecánicos y maquinaria'),
    ('Programador backend', 'Desarrolla y mantiene la lógica del lado del servidor y APIs para aplicaciones web'),
    ('Ayudante de campo',    'Apoya en labores diarias de campo y mantenimiento de huertas');