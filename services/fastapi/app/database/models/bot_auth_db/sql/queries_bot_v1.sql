-- ********************************
-- TEST ELIMINACION DE UN CATEGORIA
-- ********************************

-- bot_categories
SELECT
    id, name, description
FROM
    bot_categories;


-- bot_category_link
SELECT
    *
FROM bot_category_link;

-- Borrar una categoría específica
DELETE FROM bot_categories
WHERE id = 2;



-- **************************
-- TEST ELIMINACION DE UN BOT
-- **************************

-- bots
SELECT
    id, name, description, bot_model_id, status_id, environment_id
FROM
    bots;

-- bot_credentials
SELECT
    id, bot_id, hashed_password
FROM bot_credentials;

-- boot_category_link
SELECT
    *
FROM bot_category_link;

-- Borrar un bot específico
DELETE FROM bots
WHERE id = 2;