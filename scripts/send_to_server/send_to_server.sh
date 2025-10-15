#!/usr/bin/env bash
# ==============================================================================
# DESCRIPCIÓN
#   Este script sincroniza (sube) el contenido del directorio donde se encuentra
#   el propio script hacia un directorio remto en un servido, usando rsync.
#
# USO
#   1) Ajusta las variables de la sección CONFIG.
#   2) Dale permisos de ejecución:
#        chmod +x send_to_server.sh
#   2) Ejecuta el script:
#        ./send_to_server.sh
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
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_ROOT="$SCRIPT_DIR"

# Nombre del propio script (para excluirlo)
SELF_NAME="$(basename "$0")"

# Flags para rsync
RSYNC_FLAGS=(
    -avz                          # archive (permisos/fechas), verbose, compress
    --human-readable              # tamaños legibles
    --info=progress2,stats2       # progreso global + estadísticas
    --rsh="ssh -p $SSH_PORT"      # usa SSH con el puerto indicado
    --exclude="$SELF_NAME"        # ⛔ no subir este script
)

echo "🚀 Sincronizando archivos"
echo "   Local : $LOCAL_DIR"
echo "   Remoto: $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"
echo


# IMPORTANTE:
# - "$LOCAL_DIR"/ con slash final => copia SOLO el contenido del directorio local.
# - "$REMOTE_DIR"/ puede crearse si la ruta padre existe y tienes permisos.
rsync "${RSYNC_FLAGS[@]}" "$LOCAL_DIR"/ "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

# Fin
