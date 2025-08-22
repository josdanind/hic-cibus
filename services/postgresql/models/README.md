# 📦 Carpeta `models/`

Este directorio contiene las carpetas organizadas por **base de datos**. Cada subcarpeta agrupa los archivos `.sql` relacionados con la estructura, modelos o catálogos de una base de datos específica.

---

## 📂 Organización

Cada subcarpeta representa una base de datos o un módulo lógico. Dentro de ellas deben almacenarse los scripts `.sql` que definen:

- La estructura de la base de datos (tablas, índices, relaciones)
- Datos iniciales (catálogos, valores por defecto)
- Secuencia de ejecución (usando prefijos numéricos)

Ejemplo:

```
models/
├── crud_users_db/
│   └── 01_create_tables.sql
├── mqtt_users_db/
│   └── 02_seed_data.sql
└── tlaloc_core_db/
    ├── 01_models.sql
    ├── 02_catalogs.sql
    └── tlaloc_db_backup.sql  ← ❌ será ignorado
```

---

## 🚫 Reglas de Git (.gitignore)

Para mantener el repositorio limpio y controlado, se ha definido una estrategia de exclusión de archivos basada en reglas de `.gitignore`:

- 🔒 **Todos los archivos `.sql` serán ignorados por defecto**.
- ✅ **Solo se incluirán en el repositorio los archivos `.sql` que comiencen con un número** (`0-9`).

Esto permite:
- Llevar control de versiones explícito usando prefijos ordenados (`01_`, `02_`, etc.).
- Evitar la inclusión de respaldos, archivos temporales o pruebas locales.

---

## ✅ Buenas prácticas

- Usa prefijos numéricos en el nombre de los scripts para mantener un orden lógico de ejecución:
  - `01_create_schema.sql`
  - `02_insert_catalogs.sql`
- No prefijes con número los archivos que **no deseas versionar** (como backups, pruebas, o borradores).
- Si lo deseas, puedes incluir un `README.md` dentro de cada subcarpeta para documentar el contenido de esa base/módulo.

---

## 📌 Importante

El archivo `.gitignore` está ubicado en la carpeta `models/` y aplica las reglas de exclusión para **todas sus subcarpetas**. Asegúrate de nombrar correctamente tus archivos para que se incluyan o excluyan según corresponda.
