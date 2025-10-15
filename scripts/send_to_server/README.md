# 📂 Script de sincronización de configuraciones

Este script permite **sincronizar (subir)** los archivos de configuración locales —por ejemplo `.env` o configuraciones asociadas a contenedores— hacia un directorio remoto en un servidor, **manteniendo la misma estructura de carpetas** del proyecto.

---

## 🚀 Cómo usarlo

1. **Ubicación**
   Coloca el script en la **raíz del proyecto local**, donde tengas la misma estructura que en el servidor.
   Ejemplo:
   ```
   services/postgresql/.env
   services/api/.env
   send_to_server.sh
   ```

2. **Configura los parámetros de conexión en el script:**
   ```bash
   REMOTE_USER="usuario"          # usuario remoto del servidor
   REMOTE_HOST="mi-servidor.com"  # dominio o IP del servidor
   SSH_PORT=22                    # puerto SSH (22 por defecto)
   REMOTE_DIR="/home/usuario/mi-repo"  # ruta en el servidor donde se subirán los archivos
   ```

3. **Dale permisos de ejecución al script:**
   ```bash
   chmod +x send_to_server.sh
   ```

4. **Ejecuta el script:**
   ```bash
   ./send_to_server.sh
   ```

   Esto iniciará la sincronización de todos los archivos del directorio donde se encuentra el script hacia el servidor remoto, usando `rsync` sobre SSH.

---

## 📌 Qué hace

- Usa `rsync` para copiar todos los archivos del proyecto local al servidor remoto.
- Mantiene intacta la **estructura de carpetas**.
- Excluye automáticamente el propio script (`send_to_server.sh`).
- Muestra progreso detallado y estadísticas de transferencia.
- Si el directorio remoto no existe, `rsync` lo crea (si tienes permisos suficientes).

Ejemplo:
```
local/services/postgresql/.env  →  remoto:/home/usuario/mi-repo/services/postgresql/.env
```

---

## 🛡️ Seguridad y robustez

- El script usa las opciones:
  - `set -e` → detiene la ejecución si un comando falla.
  - `set -u` → error si se usa una variable no definida.
  - `set -o pipefail` → falla si cualquier comando dentro de un *pipe* falla.
- Usa `ssh` con autenticación por clave o contraseña.
- Puedes incluir exclusiones adicionales con más `--exclude` en la lista `RSYNC_FLAGS`.

---

## 🧩 Requisitos

- Tener `rsync` instalado tanto en el equipo local como en el servidor.
- Acceso SSH válido al servidor remoto.