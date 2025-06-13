# 🧩 Dependencias

1. **fastapi**
   Framework moderno para construir APIs web rápidas y robustas en Python. Genera automáticamente documentación interactiva con Swagger y Redoc.

2. **uvicorn[standard]**
   Servidor ASGI rápido y ligero para ejecutar aplicaciones FastAPI. El extra `[standard]` incluye mejoras de rendimiento como `uvloop`, `httptools`, y `websockets`.

3. **rich**
   Biblioteca para mostrar texto enriquecido en la terminal, incluyendo colores, tablas, barras de progreso y trazas de error más legibles.

4. **sqlmodel**
   ORM moderno basado en SQLAlchemy y Pydantic. Facilita la definición de modelos y el trabajo con bases de datos en aplicaciones FastAPI.

5. **PyJWT**
   Permite crear y verificar tokens JWT (JSON Web Tokens), comúnmente utilizados para autenticación y autorización en APIs.

6. **passlib**
   Biblioteca para el manejo seguro de contraseñas, soportando múltiples algoritmos de hashing como bcrypt, pbkdf2, entre otros.

7. **Jinja2**
   Motor de plantillas para Python, útil para renderizar HTML dinámico desde FastAPI u otros entornos web.

8. **python-multipart**
   Necesaria para que FastAPI procese formularios `multipart/form-data`, como los usados en la carga de archivos.

---

## 📦 Instalación

```bash
pip install fastapi "uvicorn[standard]" rich sqlmodel PyJWT passlib jinja2 python-multipart
```