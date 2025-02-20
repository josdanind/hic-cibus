<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://i.imgur.com/KB6cqcf.jpeg" alt="hic-cibus"></a>
</p>
<p align="center">
    <em>hic-cibus: Una biblioteca libre y gratuita que recopila y comparte estrategias, manuales y herramientas digitales para documentar, replicar y crear procesos innovadores.</em>
</p>

---

## 🛡️ **Rama:**  `infra/docker-traefik/fastapi`

Esta rama proporciona una configuración predefinida para desplegar un servicio FastAPI integrado con Traefik como proxy inverso. Está diseñada para ofrecer una base lista para el desarrollo de APIs en entornos de desarrollo y producción, facilitando la implementación de routers y brindando soporte para HTTPS.

En resumen, se ha configurado un servicio Docker con una API FastAPI lista para agregar routers y comenzar a trabajar. Gracias a Traefik, el servicio admite HTTPS para mantener las conexiones protegidas. Además, incluye un router predefinido llamado `home`, que muestra una página web informativa.

> ¡Crea tus endpoints de manera fácil y rápida, sin preocuparte por la infraestructura subyacente! 🚀✨

### 📂 **Estructura de la Arquitectura**

```
services/
└── fastapi/
    ├── app/                                  # Directorio principal de la aplicación FastAPI
    │   ├── api/                              # Directorio para los endpoints de la API
    │   ├── core/                             # Configuraciones y utilidades centrales
    │   ├── models/                           # Modelos de datos
    │   ├── database/                         # Conexión a la base de datos y gestión de sesiones
    │   ├── schemas/                          # Esquemas de datos (Pydantic)
    │   ├── utils/                            # Funciones auxiliares y herramientas reutilizables
    ├── .dockerignore                         # Archivos ignorados por Docker
    ├── Dockerfile                            # Dockerfile para construir la imagen en producción
    ├── Dockerfile.dev                        # Dockerfile para construir la imagen en desarrollo
    ├── main.py                               # Punto de entrada de la aplicación FastAPI
    └── requirements.txt                      # Dependencias de la aplicación
└── traefik/                                  # Configuración de Traefik como reverse proxy y gestor de certificados
    └── ...                                   # Archivos de configuración de Traefik (no detallados)

├── .env                                      # Variables de entorno
├── .env.example                              # Ejemplo de archivo de variables de entorno
├── .gitignore                                # Archivos ignorados en Git
├── docker-compose-traefik-fastapi-dev.yml    # Docker Compose para ejecutar la API en desarrollo
├── docker-compose-traefik-fastapi.yml        # Docker Compose para ejecutar la API en producción
├── docker-compose-traefik-dev.yml            # Docker Compose para entorno de desarrollo
├── docker-compose-traefik.yml                # Docker Compose para producción
├── LICENSE                                   # Licencia del proyecto
├── README.md                                 # Documentación de la rama
├── scripts/                                  # Directorio para scripts
│   ├── send_files_to_server.sh               # Script para enviar archivos al servidor
├── docs/                                     # Documentación
│   ├── droplet_config.md                     # Configuración inicial de un Droplet en DigitalOcean
```

---
