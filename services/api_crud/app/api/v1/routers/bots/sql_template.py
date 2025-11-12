"""
Modulo: sql_template.py

Este modulo encapsula toda la lógica para:

1. Recuperar la plantilla SQL almacenada en la base de datos.
2. Validar y preparar los parámetros que necesita.
3. Ejecutar con seguridad (sin concatenar strings peligrosos).
4. Devolver los resultados.
"""
# Librería estándar
import re
from typing import Any, Dict, Iterable

_BIND_RE = re.compile(r":([a-zA-Z_][a-zA-Z0-9_]*)")

def _extract_bind_name(sql:str) -> set[str]:
    return set(_BIND_RE.findall(sql))

def _quote_ident_pg(ident: str) -> str:
    return '"' + ident.replace('"', '""') + '"'

def inject_identifiers(
    sql: str,
    identifiers: Dict[str, str],
    *,
    whitelist: Dict[str, Iterable[str]]|None=None
) -> str:
    """
    Inyecta identificadores (por ejemplo, nombres de tablas o columnas) en una
    plantilla SQL.
    """
    def repl(match: re.Match[str]) -> str:
        name = match.group(1)

        # 1. Validar que existe
        if name not in identifiers:
            raise ValueError(f"Falta identificador '{name}'")

        value = identifiers[name]

        # 2. Validar contra whitelist si se especifica
        if whitelist is not None:
            allowed = set(whitelist.get(name, []))
            if value not in allowed:
                raise ValueError(f"Identificador '{name}' con valor no permitido: {value}")

        # 3. Escapar el valor como identificador de PostgreSQL
        return _quote_ident_pg(value)

    return re.sub(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}", repl, sql)

