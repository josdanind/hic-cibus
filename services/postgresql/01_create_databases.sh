#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Crea las bases de datos
	CREATE DATABASE $BOT_AUTH_DB;
	CREATE DATABASE $USER_AUTH_DB;
	CREATE DATABASE $MQTT_AUTH_DB;
EOSQL
