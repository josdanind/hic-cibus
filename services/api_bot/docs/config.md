# 🧩 Dependencias

1. **fastapi**
   Framework moderno y eficiente para construir APIs web usando Python 3.7+ con validación automática y documentación integrada (OpenAPI, Swagger).

2. **uvicorn[standard]**
   Servidor ASGI ultrarrápido para ejecutar aplicaciones FastAPI. El extra `[standard]` incluye optimizaciones como `uvloop`, `httptools`, y `websockets`.

3. **rich**
   Biblioteca para imprimir texto enriquecido en la terminal: colores, tablas, barras de progreso y trazas de errores más legibles.

4. **python-multipart**
   Necesaria para que FastAPI procese formularios `multipart/form-data`, comúnmente usados en carga de archivos.

5. **pydantic-settings**
   Extensión de Pydantic para manejar configuraciones cargadas desde archivos `.env` o variables de entorno.

6. **redis**
   Cliente para conectarse a bases de datos Redis (o Valkey), útil como sistema de caché, manejo de sesiones o almacenamiento temporal de tokens.

7. **aiohttp**
   Cliente HTTP asíncrono para realizar solicitudes externas de manera no bloqueante, ideal para microservicios y comunicación entre APIs.

---

## 📦 Instalación

```bash
pip install fastapi "uvicorn[standard]" rich python-multipart pydantic-settings redis aiohttp pyngrok pyTelegramBotAPI
```
