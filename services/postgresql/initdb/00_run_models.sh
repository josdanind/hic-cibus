#!/usr/bin/env bash
set -euo pipefail
#
# 00_run_models.sh
# ---------------------------------------------------------------------------
# Propósito
#   - Detectar todas las subcarpetas de "models" (hermana de "initdb").
#   - Crear una base de datos por cada subcarpeta (nombre de la carpeta = nombre de la BD).
#   - Ejecutar los scripts SQL de cada carpeta en orden determinista:
#       1) Obligatorios: NN_*.sql  (01_, 02_, 10_, …) → PRIMERO (definen lógica base).
#       2) Semillas/usuario: *.sql SIN prefijo NN_    → DESPUÉS (datos por instancia).
#
# Contexto de ejecución
#   - Coloca este script en /docker-entrypoint-initdb.d (carpeta "initdb").
#   - El entrypoint oficial de PostgreSQL lo ejecuta SOLO en el primer arranque
#     (cuando el volumen de datos está vacío). Por eso CREATE DATABASE puede asumir
#     que la BD no existe aún.
#
# Requisitos (variables de entorno)
#   - POSTGRES_USER : usuario que la imagen de PostgreSQL CREA en el primer arranque.
#   - POSTGRES_DB   : Nombre de la base de datos que  va a contener la lógica
# ---------------------------------------------------------------------------

# 📍 Ruta ABS del directorio del script (no depende del CWD)
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd -P)"

# 🤝 "models" al MISMO nivel que "initdb"
MODELS_ROOT="$(cd "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd -P)/models"

if [ ! -d "$MODELS_ROOT" ]; then
    echo "❌ No existe el directorio de modelos: $MODELS_ROOT" >&2
    exit 1
fi

# 📚 Recolectar NOMBRES de subcarpetas (primer nivel) en un ARRAY con mapfile
# - find … -printf '%f\0' → imprime solo el nombre base de cada carpeta, separado por NUL
# - sort -z               → orden determinista respetando el separador NUL    → orden determinista respetando separador NUL
mapfile -d '' MODEL_DIRS < <(
    find "$MODELS_ROOT" -mindepth 1 -maxdepth 1 -type d -printf '%f\0' | LC_ALL=C sort -z
)

# 🟩 Sin subcarpetas → terminar en verde
if (( ${#MODEL_DIRS[@]} == 0 )); then
    echo "ℹ️ No hay subcarpetas dentro de: $MODELS_ROOT"
    exit 0
fi

echo "🚧 Creando bases de datos..."
for DB_NAME in "${MODEL_DIRS[@]}"; do
    echo "● $DB_NAME"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE DATABASE "$DB_NAME" OWNER "$POSTGRES_USER";
EOSQL

    SQL_DIR="$MODELS_ROOT/$DB_NAME"

    # 📄 Construcción de la lista de ficheros SQL a ejecutar
    mapfile -d '' SQL_FILES < <(
        {
            # 1) Obligatorios (NN_*.sql) primero, orden natural
            find "$SQL_DIR" -maxdepth 1 -type f -name '[0-9][0-9]_*.sql' -print0 | LC_ALL=C sort -zV
            # 2) Semillas/usuario (sin prefijo)
            find "$SQL_DIR" -maxdepth 1 -type f -name '*.sql' ! -name '[0-9][0-9]_*.sql' -print0 | LC_ALL=C sort -z
        }
    )

    # 🟨 Si no hay .sql en esta carpeta, continuar con la siguiente BD
    if (( ${#SQL_FILES[@]} == 0 )); then
        echo "ℹ️ No hay archivos .sql en $SQL_DIR"
        continue
    fi

    # 📜 Ejecución de los scripts SQL
    echo "▶ Ejecutando ficheros SQL ..."
    for file in "${SQL_FILES[@]}"; do
        echo "   ▶ $file"
        psql -v ON_ERROR_STOP=1 \
            --username "$POSTGRES_USER" \
            --dbname "$DB_NAME" \
            -f "$file"
    done

    echo "✓ BD $DB_NAME lista."
done
