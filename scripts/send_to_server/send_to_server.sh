#!/usr/bin/env bash
set -euo pipefail

# ============ CONFIG ============
REMOTE_USER="tu_usuario"
REMOTE_HOST="tu_dominio.com"
SSH_PORT=22
REMOTE_ROOT="ruta_servirdor"   # raíz del repo en el servidor

# Raíz local = carpeta donde está el script
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_ROOT="$SCRIPT_DIR"

# =================================

# Nombre del propio script (para excluirlo)
SELF_NAME="$(basename "$0")"

RSYNC_FLAGS=(
    -avz                       # archive, verbose, compress
    --human-readable
    --info=progress2,stats2
    --rsh="ssh -p $SSH_PORT"
    --exclude="$SELF_NAME"     # ⛔ no enviar este script
)

echo "🚀 Enviando ficheros desde:"
echo "   Local : $LOCAL_ROOT"
echo "   Remoto: $REMOTE_USER@$REMOTE_HOST:$REMOTE_ROOT"
echo

rsync "${RSYNC_FLAGS[@]}" "$LOCAL_ROOT"/ "$REMOTE_USER@$REMOTE_HOST:$REMOTE_ROOT/"
