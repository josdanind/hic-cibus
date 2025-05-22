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
