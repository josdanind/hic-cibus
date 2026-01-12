# 📂 Script de sincronización de configuraciones
## sync-config-files.sh

Este script permite **sincronizar archivos de configuración locales** hacia un servidor remoto usando **rsync sobre SSH**, manteniendo **exactamente la misma estructura de carpetas** entre el entorno local y el servidor.

Está diseñado para proyectos con **múltiples servicios** (Traefik, base de datos, APIs, bots, etc.), donde cada servicio posee sus propios archivos de configuración como `.env`, `docker-compose.yml`, archivos YAML, entre otros.

---

## 🎯 Objetivo

Disponer de una forma **simple, segura e interactiva** de enviar configuraciones al servidor remoto sin:

- Copiar archivos manualmente
- Romper la estructura del proyecto
- Subir archivos innecesarios
- Afectar el código fuente

---

## 🗂️ Estructura esperada del proyecto

El script debe ubicarse en la **raíz del proyecto**, junto a las carpetas de cada servicio.

```text
.
├── traefik/
│   └── .env
├── database/
│   └── .env
├── crud-api/
│   └── .env
├── telegram-bot-api/
│   └── .env
└── sync-config-files.sh
```

El servidor remoto debe mantener la misma estructura base:

```text
/home/usuario/Tlaloc/
├── traefik/
├── database/
├── crud-api/
└── telegram-bot-api/
```


## 🚀 Cómo usarlo

### 1️⃣ Configuración de conexión

Edita la sección CONFIG dentro del script:

```bash
REMOTE_USER="usuario"
REMOTE_HOST="mi-servidor.com"
SSH_PORT=22
REMOTE_DIR="/home/usuario/Tlaloc"
```

### 2️⃣ Dar permisos de ejecución

```bash
chmod +x sync-config-files.sh
```

### 3️⃣ Ejecutar el script

```bash
./sync-config-files.sh
```

Se mostrará un menú interactivo:

```text
🚀 Enviar configuración de:
   1) Traefik
   2) Database
   3) CRUD API
   4) Bot API
   5) Todos
```

Selecciona la opción deseada y el script sincronizará solo el servicio elegido o todos.

## 📌 Qué hace

- Sincroniza archivos de configuración usando rsync

- Mantiene permisos, fechas y estructura de carpetas

- Excluye automáticamente el propio script

- Muestra progreso y estadísticas de transferencia

Ejemplo de sincronización:

```text
local/traefik/.env
→
remoto:/home/usuario/Tlaloc/traefik/.env
```