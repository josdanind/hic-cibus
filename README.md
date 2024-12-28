<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://i.imgur.com/KB6cqcf.jpeg" alt="hic-cibus"></a>
</p>
<p align="center">
    <em>hic-cibus: Una biblioteca libre y gratuita que recopila y comparte estrategias, manuales y herramientas digitales para documentar, replicar y crear procesos innovadores.</em>
</p>

---

## 🛡️ **Rama:**  `infra/dockerTraefik/base`

Esta rama contiene la configuración base para integrar Docker y Traefik, proporcionando un proxy inverso para gestionar los servicios en dos entornos diferenciados: Desarrollo y Producción. Además, la API de Traefik está habilitada para monitoreo y control de las configuraciones de tráfico.

### 📂 **Estructura del Proyecto**

```
services/
└── traefik/
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

---
