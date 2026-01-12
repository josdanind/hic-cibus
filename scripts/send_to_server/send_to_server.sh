#!/usr/bin/env bash
# ==============================================================================
# DESCRIPCIÓN
#   Script interactivo para sincronizar archivos de configuración locales hacia
#   un servidor remoto mediante rsync sobre SSH.
#
# USO
#   1) Ajusta las variables de la sección CONFIG según tu servidor.
#   2) Da permisos de ejecución al script:
#        chmod +x sync-config-files.sh
#   3) Ejecuta el script:
#        ./sync-config-files.sh
#   4) Selecciona el componente que deseas sincronizar.
#
# SEGURIDAD/ROBUSTEZ
#   - set -euo pipefail:
#       -e → termina el script si un comando falla.
#       -u → error si se usa una variable no definida.
#       -o pipefail → falla si cualquiera de los comandos en un pipe falla.
# ==============================================================================

set -euo pipefail

# ============ CONFIG ==========================================================
# Usuario remoto de SSH (ajústalo a tu usuario del servidor)
REMOTE_USER="tu_usuario"

# Host o dominio del servidor remoto (ej.: "example.com" o "192.0.2.10")
REMOTE_HOST="tu_dominio.com"

# Puerto SSH (22 por defecto; cambia si tu servidor usa otro)
SSH_PORT=22

# Directorio raíz destino en el servidor.
REMOTE_DIR="directorio_remoto"
# ==============================================================================

# Directorio local a sincronizar = carpeta donde está este script
LOCAL_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# Nombre del script (para excluirlo)
SCRIPT_NAME="$(basename "$0")"

# Flags para rsync
RSYNC_FLAGS=(
    -avz                          # archive (permisos/fechas), verbose, compress
    --human-readable              # tamaños legibles
    --info=progress2,stats2       # progreso global + estadísticas
    --rsh="ssh -p $SSH_PORT"      # usa SSH con el puerto indicado
    --exclude="$SCRIPT_NAME"        # ⛔ no subir este script
)

echo "🚀 Enviar configuración de:"
echo "   1) Traefik"
echo "   2) Database"
echo "   3) CRUD API"
echo "   4) Bot API"
echo "   5) Todos"
echo

read -p "Seleccione una opción: " CONTAINER

case $CONTAINER in
  1)
    FOLDER="traefik"
    LOCAL_DIR="$LOCAL_DIR/$FOLDER"
    ;;
  2)
    FOLDER="database"
    LOCAL_DIR="$LOCAL_DIR/$FOLDER"
    ;;
  3)
    FOLDER="crud-api"
    LOCAL_DIR="$LOCAL_DIR/$FOLDER"
    ;;
  4)
    FOLDER="telegram-bot-api"
    LOCAL_DIR="$LOCAL_DIR/$FOLDER"
    ;;
  5)
    FOLDER=""
    LOCAL_DIR="$LOCAL_DIR"
    ;;
  *)
    echo "Opción inválida"
    exit 1
    ;;
esac

echo $LOCAL_DIR
rsync "${RSYNC_FLAGS[@]}" "$LOCAL_DIR/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/$FOLDER/"
