<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://i.imgur.com/KB6cqcf.jpeg" alt="hic-cibus"></a>
</p>
<p align="center">
    <em>hic-cibus: Una biblioteca libre y gratuita que recopila y comparte estrategias, manuales y herramientas digitales para documentar, replicar y crear procesos innovadores.</em>
</p>

---

## 🛡️ **Rama:**  `infra/dockerTraefik/base`

Esta rama contiene la configuración base para integrar Docker y Traefik, proporcionando un proxy inverso para gestionar los servicios en dos entornos diferenciados: Desarrollo y Producción. Además, la API de Traefik está habilitada para monitoreo y control de las configuraciones de tráfico.

En otras palabras, aquí se propone una arquitectura Docker donde uno de los contenedores principales es Traefik. Este contenedor se encarga de enrutar las peticiones HTML usando subdominios, redirigiendo el tráfico a los contenedores correspondientes de Docker. Así, cada servicio puede operar de manera independiente y coordinada bajo el mismo dominio.

#### Ejemplo:

- **Dominio Completo:** `mi_api.tu_dominio.com`
- **Sub Dominio:** `mi_api`
- **Función:** Traefik enruta las solicitudes HTTP/HTTPS al contenedor de la API correspondiente, identificado por el subdominio `mi_api`.

### 📂 **Estructura de la Arquitectura**

```
services/                           # Directorio para los servicios.
└── traefik/                        # Configuración específica de Traefik
    ├── traefik-dev.toml            # Configuración de Traefik para entorno de desarrollo
    ├── traefik.toml                # Configuración principal de Traefik

├── .env                            # Variables de entorno
├── .env.example                    # Ejemplo de archivo de variables de entorno
├── .gitignore                      # Archivos ignorados en Git
├── docker-compose-traefik-dev.yml  # Docker Compose para entorno de desarrollo
├── docker-compose-traefik.yml      # Docker Compose para producción
├── LICENSE                         # Licencia del proyecto
├── README.md                       # Documentación de la rama
```

### 📚 Descripción General

#### Configuraciones estáticas de Traefik:

- Utilizar `traefik-dev.toml` para el entorno de desarrollo.
- Utilizar `traefik.toml` para el entorno de producción.

#### Configuraciones de Docker y Traefik (routers, middlewares, servicions):

- Utilizar `docker-compose-traefik-dev.yml` para el entorno de desarrollo.
- Utilizar `docker-compose-traefik.yml` para el entorno de producción.

#### API de Traefik

- Habilitada en ambos entornos para monitoreo y control.
- Acceso a la API a través del Dashboard de Traefik.
  - `traefik-dev.tu_dominio.com` Entorno de desarrollo.
  - `traefik.tu_dominio.com` Entorno de producción.

### 🚀 Instrucciones de Uso
---
