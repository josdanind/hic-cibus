<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://i.imgur.com/KB6cqcf.jpeg" alt="hic-cibus"></a>
</p>
<p align="center">
    <em>hic-cibus: Una biblioteca libre y gratuita que recopila y comparte estrategias, manuales y herramientas digitales para documentar, replicar y crear procesos innovadores.</em>
</p>

---
# 🌾 Tlaloc: Aplicación de Monitorización de Cultivos

Tlaloc es una aplicación diseñada para la monitorización y gestión de cultivos. Este repositorio contendrá las diferentes componentes y servicios que conforman esta aplicación, organizada en ramas específicas para cada funcionalidad o infraestructura.

## 🐘 **Rama:**  `tlaloc/postgresql` - Servicio de Base de Datos PostgreSQL

Esta rama se enfoca en la implementación y configuración del servicio de base de datos PostgreSQL para la aplicación Tlaloc. Aquí encontrarás la definición y la estructura necesaria para soportar los datos de varios componentes de la aplicación.

Se configura un servidor PostgreSQL que contiene tres bases de datos:

1. **Autenticación de Bots:** Para credenciales y datos de bots.
2. **Usuarios API CRUD:** Para usuarios con acceso a la API CRUD de Tlaloc.
3. **Usuarios MQTT:** Para información de usuarios del broker MQTT.

Esta base de datos es fundamental para la autenticación y gestión de bots, la API CRUD y el broker MQTT, centralizando el almacenamiento de datos.


### 📂 **Estructura de la Arquitectura**
---

```
.
├── .env.example                       # Ejemplo de archivo de variables de entorno
├── .gitignore                         # Archivos ignorados en Git
├── docker-compose-postgresql-dev.yml  # Docker Compose para PostgreSQL en desarrollo
├── docker-compose-postgresql.yml      # Docker Compose para PostgreSQL en producción
├── docker-compose-traefik-dev.yml     # Docker Compose para Traefik en desarrollo
├── docker-compose-traefik.yml         # Docker Compose para Traefik en producción
├── LICENSE                            # Licencia del proyecto
├── README.md                          # Documentación de la rama
├── scripts                            # Directorio para scripts
│   └── send_files_to_server.sh
├── docs                               # Documentación
│   └── droplet_config.md
└── services                           # Directorio para los servicios
    ├── postgresql                     # Configuración específica de PostgreSQL
    │   ├── 01_create_databases.sh     # Script para crear las 3 BDs
    │   ├── 02_models_bot_auth.sql     # Modelos/Schemas para autenticación de bots
    │   ├── 03_models_user_auth.sql    # Modelos/Schemas para usuarios de la API CRUD
    │   ├── 04_models_mqtt_user.sql    # Modelos/Schemas para usuarios MQTT
    │   ├── 05_values_bot_auth.sql     # Datos iniciales para autenticación de bots
    │   └── 06_values_user_auth.sql    # Datos iniciales para usuarios de la API CRUD
    └── traefik                        # Configuración de Traefik
        ├── auth
        │   ├── README.md
        │   └── usersFile.example
        ├── middlewares
        │   ├── middlewares-dev.toml
        │   └── middlewares.toml
        ├── traefik-dev.toml
        └── traefik.toml
```

### 📚 Descripción General
---

#### Configuración de PostgreSQL:

* El servicio PostgreSQL se define en `docker-compose-postgresql-dev.yml` (para desarrollo) y `docker-compose-postgresql.yml` (para producción).

* Los scripts de inicialización en `services/postgresql/` (`01_create_databases.sh`, `02_models_bot_auth.sql`, etc.) se ejecutan al iniciar el contenedor para crear las tres bases de datos necesarias y aplicar sus respectivos esquemas y datos iniciales.

* Las credenciales y configuraciones de conexión para PostgreSQL deben establecerse en el archivo `.env`.

### 🚀 Instrucciones de Uso
---

Para poner en marcha los servicios de la aplicación Tlaloc, sigue estos pasos:

**⚠️ Importante:** Si vas a utilizar servicios que dependen de Traefik (como las APIs), asegúrate de que el **router de Traefik esté iniciado primero**. Las instrucciones para configurar e iniciar Traefik se encuentran en la rama [`tlaloc/traefik`](https://github.com/josdanind/hic-cibus/tree/tlaloc/traefik).


#### 1. Configuración de Variables de Entorno

Primero, necesitas preparar tu archivo de variables de entorno.

* **Copia el archivo de ejemplo:** Duplica el archivo `.env.example` y renómbralo a `.env` en la raíz del proyecto:

    ```bash
    cp .env.example .env
    ```

* **Edita el archivo `.env`:** Abre el nuevo archivo `.env` y diligencia las variables de entorno según tu configuración deseada:

  * **Para PostgreSQL:** Configura los nombres de las tres bases de datos (BOT_AUTH_DB, USER_AUTH_DB, MQTT_AUTH_DB). Define las credenciales para el entorno de desarrollo (POSTGRES_USER_DEV, POSTGRES_PASSWORD_DEV, POSTGRES_DB_DEV) y asegúrate de actualizar POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB con tus valores de producción.

  **Ejemplo de `.env` (tras la edición y añadiendo las de PostgreSQL):**

   ```ini
    # ============================================================================
    #                                🌐 .env File
    # ============================================================================
    # Este archivo define las variables de entorno para la configuración de
    # servicios en Docker Compose, específicamente relacionados con el proxy
    # inverso Traefik y la base de datos de PostgreSQL.
    #
    # 🚨 IMPORTANTE:
    # 1. En entornos de producción, sustituye "hic-cibus.com" por tu dominio real.
    # 2. En entornos de desarrollo, incluye las siguientes entradas en el archivo:
    #    - Linux: `/etc/hosts`
    #    - Windows: `C:\Windows\System32\drivers\etc\hosts`
    #
    #    127.0.0.1 traefik-dev.hic-cibus.com
    #
    # 3. Si deseas usar un dominio personalizado, reemplaza "hic-cibus.com" con
    #    tu propio dominio en todas las variables correspondientes.
    # ============================================================================
    # ************************
    # 🌍 Configuración General
    # ************************
    # Zona horaria
    TZ="America/Bogota"


    # ***************************
    # 🛠️ CONFIGURACIÓN DE TRAEFIK
    # ***************************
    # =========================================================
    # 🌱 Desarrollo - docker-compose-traefik-dev.yml
    # =========================================================
    # Credenciales para el dashboard de Traefik en desarrollo (usuario: admin, contraseña: admin).
    # Dominio para acceder al dashboard de Traefik en desarrollo.
    TRAEFIK_DASHBOARD_DOMAIN_DEV="traefik-dev.hic-cibus.com"

    # ===========================================
    # 🌐 Producción - docker-compose-traefik.yml
    # ===========================================
    # Dominio para acceder al dashboard de Traefik en producción.
    TRAEFIK_DASHBOARD_DOMAIN="traefik.tu_dominio.com"

    # El archivo `usersFile` con las credenciales de producción debe almacenarse en:
    # `./services/traefik/auth/usersFile`.
    # Puedes agregar varios usuarios generando sus hashes con `htpasswd -nb <usuario> <contraseña>`.


    # *****************************
    # 🛠️ CONFIGURACIÓN DE POSGRESQL
    # *****************************
    # ===============================
    # BASES DE DATOS DE AUTENTICACIÓN
    # ===============================
    BOT_AUTH_DB="bot_auth_db"
    USER_AUTH_DB="user_auth_db"
    MQTT_AUTH_DB="mqtt_auth_db"

    # =================================================
    # 🌱 Desarrollo - docker-compose-postgresql-dev.yml
    # =================================================
    # Configuración de la base de datos para PostgreSQL en desarrollo.
    POSTGRES_USER_DEV="admin"
    POSTGRES_PASSWORD_DEV="admin"
    POSTGRES_DB_DEV="hic_cibus_dev"

    # =============================================
    # 🌐 Producción - docker-compose-postgresql.yml
    # =============================================
    # Configuración de la base de datos para PostgreSQL en producción
    POSTGRES_USER="tu_usuario"
    POSTGRES_PASSWORD="tu_contraseña"
    POSTGRES_DB="tu_base_de_datos"


    # 📌 NOTA:
    # En producción, asegúrate de que el dominio está correctamente configurado en tu DNS.
    # Mantén las credenciales en secreto para garantizar la seguridad del sistema.
    ```


#### 2. Despliegue de Servicios con Docker Compose

Una vez configurado tu archivo .env, puedes levantar los servicios:

* **Levantar el servicio Traefik:** Solo necesitas asegurarte de que Traefik esté ya corriendo (ejecutado desde su propia rama o configuración principal), ya que los servicios de esta rama (tlaloc/postgresql) no lo inician directamente.

* **Levantar el servicio PostgreSQL:**
    * **Para Desarrollo:** Para iniciar la base de datos en el entorno de desarrollo, usa el archivo `docker-compose-postgresql-dev.yml`:

        ```bash
        docker compose -f docker-compose-postgresql-dev.yml up -d
        ```

    * **Para Producción:** Para iniciar la base de datos en el entorno de producción, usa el archivo `docker-compose-postgresql.yml`:
        ```bash
        docker compose -f docker-compose-postgresql.yml up -d
        ```


#### 3. Verificación del Servicio PostgreSQL

* Puedes verificar que el contenedor de PostgreSQL se está ejecutando correctamente con:

    ```bash
    docker ps
    ```

* Para conectarte a una de las bases de datos (ej. `bot_auth_db`) y verificar su existencia o la aplicación de los esquemas, puedes usar el cliente `psql` desde tu máquina local o desde otro contenedor en la misma red de Docker.

    ```bash
    # Ejemplo de conexión desde tu terminal (asegúrate de tener psql instalado)
    # Para desarrollo:
    psql -h localhost -p 5433 -U ${POSTGRES_USER_DEV} -d ${BOT_AUTH_DB}

    # Para producción (conectar a tu servidor remoto):
    # psql -h <ip_de_servidor> -p 5432 -U ${POSTGRES_USER} -d ${BOT_AUTH_DB}
    ```
    Una vez conectado, puedes listar las tablas para verificar los modelos: `\dt`.
