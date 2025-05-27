#!/bin/bash
set -e


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE mqtt_user (
        id serial PRIMARY KEY,
        username text NOT NULL UNIQUE,
        password_hash  text NOT NULL,
        salt text NOT NULL,
        is_superuser boolean DEFAULT false,
        created timestamp with time zone DEFAULT NOW()
    );

    INSERT INTO mqtt_user(
        username,
        password_hash,
        salt,
        is_superuser
    ) VALUES (
        '$MQTT_ADMIN_USER_DEV',
        '$MQTT_ADMIN_USER_PASSWORD_HASH_DEV',
        '',
        true
    );
EOSQL