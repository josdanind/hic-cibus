#!/bin/bash

REMOTE_SERVER="tu_usuario@tu_dominio.com"

# Archivos locales y rutas remotas
declare -A FILE_PATHS=(
    [".env"]="/home/josdanind/hic-cibus"
    ["htpasswd"]="/home/josdanind/hic-cibus/services/traefik"
)

# Función para enviar un archivo al servidor remoto
send_file() {
    local local_path=$1
    local remote_path=$2

    # Verificar si el archivo existe
    if [ ! -f "$local_path" ]; then
        echo "Error: El archivo '$local_path' no existe."
        return 1
    fi

    # Enviar el archivo con scp
    echo "Enviando archivo '$local_path' a '$REMOTE_SERVER:$remote_path'..."
    scp "$local_path" "$REMOTE_SERVER:$remote_path"

    # Verificar el resultado del comando scp
    if [ $? -eq 0 ]; then
        echo "Archivo '$local_path' enviado exitosamente a '$remote_path'."
        return 0
    else
        echo "Error: Falló el envío de '$local_path' a '$remote_path'."
        return 2
    fi
}

# Validar configuración inicial
if [ -z "$REMOTE_SERVER" ]; then
    echo "Error: REMOTE_SERVER no está configurado."
    exit 1
fi

# Procesar los archivos
for local_path in "${!FILE_PATHS[@]}"; do
    remote_path="${FILE_PATHS[$local_path]}"
    send_file "$local_path" "$remote_path"

    # Si ocurre un error, se interrumpe el script
    if [ $? -ne 0 ]; then
        echo "Interrumpiendo la transferencia debido a un error."
        exit 1
    fi
done

echo "Todas las transferencias se completaron con éxito."