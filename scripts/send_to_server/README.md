# 📂 Script de sincronización de configuraciones

Este script permite enviar los archivos de configuración locales (por ejemplo `.env`) hacia el servidor, manteniendo la misma estructura de carpetas que el repositorio remoto.

---

## 🚀 Cómo usarlo

1. Coloca el script en la **raíz del proyecto local**, donde tengas la misma estructura de carpetas que en el servidor.  
   - Ejemplo:
     ```
     services/postgresql/.env
     services/api/.env
     ```

2. Configura en el script los datos de conexión:
   ```bash
   REMOTE_USER="usuario"
   REMOTE_HOST="ejemplo.com"
   SSH_PORT=22
   REMOTE_ROOT="/home/usuario/mi-repo"
   ```

3. Dale permiso de ejecución al script:
   ```bash
   chmod +x sync-configs.sh
   ```

4. Ejecuta el script:
   ```bash
   ./send_to_server.sh
   ```

---

## 📌 Qué hace

- Copia todos los archivos locales hacia el servidor en su **directorio correspondiente**.
- Mantiene la estructura (ejemplo: `services/postgresql/.env` → se sube a `services/postgresql/.env` en el servidor).
- Está pensado para enviar **archivos de configuración privados** a los directorios de los contenedores en el servidor.
---

## 🛠 Requisitos

- Tener `rsync` instalado en el local y en el servidor.  
- Acceso SSH al servidor.  