<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://i.imgur.com/KB6cqcf.jpeg" alt="hic-cibus"></a>
</p>
<p align="center">
    <em>hic-cibus: Una biblioteca libre y gratuita que recopila y comparte estrategias, manuales y herramientas digitales para documentar, replicar y crear procesos innovadores.</em>
</p>

---
# 🌾 Tlaloc: Aplicación de Monitorización de Cultivos

Tlaloc es una aplicación diseñada para la monitorización y gestión de cultivos. Este repositorio contendrá las diferentes componentes y servicios que conforman esta aplicación, organizada en ramas específicas para cada funcionalidad o infraestructura.

## 🚦 Rama: tlaloc/traefik - Configuración del Router

Esta rama es la primera configuración de infraestructura para la aplicación Tlaloc. Contiene la configuración base para integrar Docker y Traefik, proporcionando un proxy inverso esencial para gestionar y enrutar los servicios de Tlaloc en entornos diferenciados: Desarrollo y Producción. Además, la API de Traefik está habilitada para monitoreo y control de las configuraciones de tráfico.

En otras palabras, aquí se establece la arquitectura Docker donde Traefik es uno de los contenedores principales. Este se encarga de enrutar las peticiones HTML usando subdominios, redirigiendo el tráfico a los contenedores correspondientes de Docker que albergarán los servicios de Tlaloc. Así, cada servicio de la aplicación de monitorización de cultivos puede operar de manera independiente y coordinada bajo el mismo dominio.

Ejemplo de Enrutamiento para Tlaloc:

- **Dominio Completo:** `api-tlaloc.tu_dominio.com`
- **Sub Dominio:** `api-tlaloc`
- **Función:** Traefik enruta las solicitudes HTTP/HTTPS al contenedor de la API de Tlaloc correspondiente, identificado por el subdominio `api-tlaloc`.


### 📂 **Estructura de la Arquitectura**

```
services/                           # Directorio para los servicios de Tlaloc (aquí se añadirán más adelante).
└── traefik/                        # Configuración específica de Traefik para Tlaloc
    ├── auth/                       # Configuración de autenticación
    │   ├── README.md               # Documentación de autenticación
    │   ├── usersFile.example       # Ejemplo de archivo de usuarios
    ├── middlewares/                # Configuración de middlewares
    │   ├── middlewares-dev.toml    # Middlewares para entorno de desarrollo
    │   ├── middlewares.toml        # Middlewares para entorno de producción
    ├── traefik-dev.toml            # Configuración de Traefik para entorno de desarrollo
    ├── traefik.toml                # Configuración principal de Traefik

├── .env                            # Variables de entorno
├── .env.example                    # Ejemplo de archivo de variables de entorno
├── .gitignore                      # Archivos ignorados en Git
├── docker-compose-traefik-dev.yml  # Docker Compose para entorno de desarrollo
├── docker-compose-traefik.yml      # Docker Compose para producción
├── LICENSE                         # Licencia del proyecto
├── README.md                       # Documentación de la rama
├── scripts/                        # Directorio para scripts
│   ├── send_files_to_server.sh     # Script para enviar archivos al servidor
├── docs/                           # Documentación
│   ├── droplet_config.md           # Configuración inicial de un Droplet en DigitalOcean

```

### 📚 Descripción General

#### Configuraciones estáticas de Traefik:

- Utilizar `traefik-dev.toml` para el entorno de desarrollo.
- Utilizar `traefik.toml` para el entorno de producción.

#### Configuraciones de Docker y Traefik (routers, middlewares, servicios):

- Utilizar `docker-compose-traefik-dev.yml` para el entorno de desarrollo.
- Utilizar `docker-compose-traefik.yml` para el entorno de producción.

#### API de Traefik

- Habilitada en ambos entornos para monitoreo y control.
- Acceso a la API a través del Dashboard de Traefik.
  - `traefik-dev.tu_dominio.com` Entorno de desarrollo.
  - `traefik.tu_dominio.com` Entorno de producción.

### 🚀 Instrucciones de Uso
---

Para poner en marcha la configuración de Traefik para tu aplicación Tlaloc, sigue estos pasos:

#### 1. Configuración de Variables de Entorno

Primero, necesitas preparar tu archivo de variables de entorno.

* **Copia el archivo de ejemplo:** Duplica el archivo `.env.example` y renómbralo a `.env` en la raíz del proyecto:

    ```bash
    cp .env.example .env
    ```

* **Edita el archivo `.env`:** Abre el nuevo archivo `.env` y diligencia las variables de entorno según tu configuración deseada:

    * Asegúrate de configurar `TZ` para tu zona horaria (`America/Bogota` por defecto).

    * Para el **entorno de desarrollo**, verifica que `TRAEFIK_DASHBOARD_DOMAIN_DEV` apunte al dominio deseado (por ejemplo, `traefik-dev.hic-cibus.com`). Recuerda añadir la entrada `127.0.0.1 traefik-dev.hic-cibus.com` en tu archivo `/etc/hosts` (Linux) o `C:\Windows\System32\drivers\etc\hosts` (Windows) para que funcione localmente.

    * Para el **entorno de producción**, actualiza `TRAEFIK_DASHBOARD_DOMAIN` con tu dominio real (por ejemplo, `traefik.tu_dominio.com`).

    **Ejemplo de `.env` (tras la edición):**

    ```ini
    # ============================================================================
    #                                🌐 .env File
    # ============================================================================
    # Este archivo define las variables de entorno para la configuración de
    # servicios en Docker Compose, específicamente relacionados con el proxy
    # inverso Traefik y el servidor EMQX.
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
    TRAEFIK_DASHBOARD_DOMAIN_DEV="traefik-dev.tu_dominio.com" # <--- ¡IMPORTANTE! Cambia esto si usas un dominio distinto

    # ===========================================
    # 🌐 Producción - docker-compose-traefik.yml
    # ===========================================
    # Dominio para acceder al dashboard de Traefik en producción.
    TRAEFIK_DASHBOARD_DOMAIN="traefik.tu_dominio.com" # <--- ¡IMPORTANTE! Asegúrate de que este sea tu dominio real en producción

    # El archivo `usersFile` con las credenciales de producción debe almacenarse en:
    # `./services/traefik/auth/usersFile`.
    # Puedes agregar varios usuarios generando sus hashes con `htpasswd -nb <usuario> <contraseña>`.


    # 📌 NOTA:
    # En producción, asegúrate de que el dominio está correctamente configurado en tu DNS.
    # Mantén las credenciales en secreto para garantizar la seguridad del sistema.
    ```

#### 2. Creación del Archivo usersFile para Producción

Para el entorno de producción, es crucial asegurar el dashboard de Traefik.

* **Navega al directorio de autenticación:**

    ```bash
    cd services/traefik/auth
    ```

* **Crea el archivo `usersFile`:** Puedes copiar el ejemplo o crearlo desde cero.
   
    ```bash
    touch usersFile
    ```

* **Genera y añade usuarios**: Utiliza htpasswd (generalmente viene con Apache utils, puedes instalarlo con `sudo apt-get install apache2-utils` en Debian/Ubuntu o buscar el paquete equivalente para tu sistema).
  
  * Para crear un nuevo archivo `usersFile` con un usuario:

    ```bash
    htpasswd -cb usersFile nombre_de_usuario contraseña_segura
    ```
  * Para añadir más usuarios a un `usersFile` existente: 

    ```bash
    htpasswd -b usersFile nuevo_usuario nueva_contraseña_segura
    ```

**Ejemplo de contenido para `usersFile`**

```
usuario1:$apr1$sZ...
admin:$apr1$OtroHashDeEjemplo..
 ```

#### 3. Despliegue con Docker Compose

Una vez configurado tu archivo `.env` y el `usersFile` para producción, puedes levantar los servicios de Traefik según el entorno:

* **Para Desarrollo:**
    Utiliza el archivo `docker-compose-traefik-dev.yml`. Las credenciales del dashboard serán `admin:admin`.

    ```bash
    docker compose -f docker-compose-traefik-dev.yml up -d
    ```

* **Para Producción:**

    Asegúrate de que tu archivo `./services/traefik/auth/usersFile` exista y tenga las credenciales correctas. Utiliza el archivo `docker-compose-traefik.yml`.

    ```bash
    docker compose -f docker-compose-traefik.yml up -d
    ```

#### 4. Verificación en el Navegador

Después de levantar los servicios, puedes verificar que Traefik está funcionando correctamente:

* **Accede al Dashboard de Traefik:**
    Abre tu navegador y navega a la URL configurada para el dashboard de Traefik:
    * **Desarrollo:** `http://traefik-dev.tu_dominio.com` (reemplaza `tu_dominio.com` con el dominio que configuraste en el `.env` y añadiste en tu archivo `hosts`). Se te pedirá el usuario (`admin`) y la contraseña (`admin`).
    * **Producción:** `https://traefik.tu_dominio.com` (reemplaza `tu_dominio.com` con tu dominio real). Se te pedirá el usuario y la contraseña que configuraste en el archivo `usersFile`.

    Deberías ver el panel de control de Traefik, mostrando los *routers* y *servicios* activos. Esto confirmará que Traefik está en ejecución y listo para enrutar el tráfico a los servicios de Tlaloc cuando se desplieguen.
