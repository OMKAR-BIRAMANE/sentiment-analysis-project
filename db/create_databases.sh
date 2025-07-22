#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-EOSQL
    CREATE DATABASE auth_db;
    CREATE DATABASE storage_db;
EOSQL
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname auth_db -f /docker-entrypoint-initdb.d/init.sql
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname storage_db -f /docker-entrypoint-initdb.d/init.sql