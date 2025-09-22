-- 🏢 TODO LO RELACIONADO CON LAS EMPRESAS Y SUS EMPLEADOS

-- **************************
-- TEST ELIMINACION DE UN ROL
-- **************************
-- role
SELECT
    id, name
FROM
    roles;

-- Borrar una role específico
DELETE FROM roles
WHERE id = 1;

-- *******************************
-- TEST ELIMINACION DE UN EMPLEADO
-- *******************************
-- employess
SELECT
    id, first_name, last_name, position, company_id, role_id, created_at, updated_at
FROM
    employees;

UPDATE employees
SET last_name = 'Pijarra'
WHERE id = 2;

-- Borrar una empleado específico
DELETE FROM employees
WHERE id = 2;

-- *******************************
-- TEST ELIMINACION DE UNA EMPRESA
-- *******************************
-- companies
SELECT
    id, name, country
FROM
    companies;

-- Borrar una empresa específico
DELETE FROM companies
WHERE id = 2;

-- ******************************************
-- TEST ELIMINACION DE UN CONTACTO DE EMPRESA
-- ******************************************
-- company_contacts
SELECT
    id, is_primary, employee_id, notes
FROM
    company_contacts;

-- Borrar una contacto específico
DELETE FROM company_contacts
WHERE id = 1;

-- *****************************************
-- TEST ELIMINACION DE UN PERMISO DE USUARIO
-- *****************************************
-- bot_user_permissions
SELECT
    id, name, description
FROM
    bot_user_permissions;

-- Borrar un permiso específico
DELETE FROM bot_user_permissions
WHERE id = 1;

-- ****************************************
-- TEST ELIMINACION DE UN USUARIO DE UN BOT
-- ****************************************
-- bot_user
SELECT
    id, telegram_username, employee_id, permissions_id
FROM
    bot_users;

-- Borrar un permiso específico
DELETE FROM bot_users
WHERE id = 1;


-- 🤖 TODO LO RELACIONADO CON LOS BOTS
-- ********************************
-- TEST ELIMINACION DE BotUserLink
-- ********************************
-- bot_categories
SELECT
    user_id, bot_id
FROM
    user_bot_link;

-- **************************
-- TEST ELIMINACION DE UN BOT
-- **************************
-- bots
SELECT
    id, name, description, bot_model_id, status_id, environment_id
FROM
    bots;

-- Borrar un bot específico
DELETE FROM bots
WHERE id = 3;

-- ******************************************
-- TEST ELIMINACION DE UN ESTADO DE UN MODELO
-- ******************************************
SELECT
    id, name, description
FROM
    bot_model_statuses;

-- Borrar un estado específico
DELETE FROM bot_model_statuses
WHERE id = 1;

-- *****************************
-- TEST ELIMINACION DE UN MODELO
-- *****************************
-- bot_models
SELECT
    id, name, version, status_id
FROM
    bot_models;

-- *********************************
-- TEST ELIMINACION DE UNA CATEGORIA
-- *********************************
-- bot_categories
SELECT
    id, name, description
FROM
    bot_categories;

DELETE FROM bot_categories
WHERE id = 4;

-- *********************************
-- TEST ELIMINACION DE BOT CATEGORIA
-- *********************************
-- bot_category_link
SELECT
    bot_id, category_id
FROM
    bot_category_link;