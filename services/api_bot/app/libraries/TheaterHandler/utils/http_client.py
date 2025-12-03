# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería estándar
import json
from typing import Any, Literal, Protocol, AsyncIterator
from contextlib import asynccontextmanager

# 🧩 Terceros
import asyncio
import aiohttp
from aiohttp import ClientSession, ClientError, ClientResponseError

HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

class HttpClient(Protocol):
    """
    Contrato (interfaz estructural) para un cliente HTTP.
    Cualquier objeto que exponga estos métodos es compatible.
    """
    async def request(
        self,
        method: HttpMethod,
        path: str,
        /,
        **kwargs
    ) -> Any: ...
    async def get(self, path: str, /, **kwargs) -> Any: ...
    async def post(self, path: str, /, **kwargs) -> Any: ...
    async def put(self, path: str, /, **kwargs) -> Any: ...
    async def patch(self, path: str, /, **kwargs) -> Any: ...
    async def delete(self, path: str, /, **kwargs) -> Any: ...

class APIClient:
    """
    Implementación concreta del contrato HttpClient usando aiohttp.
    - Maneja sesión compartida (async with).
    - Parseo automático: JSON -> dict/list; de lo contrario -> str.
    - Puedes pasar params=, json=, data=, headers= por llamada.
    """
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str] | None = None,
        timeout_s: float = 15.0
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._headers = headers or {}
        self.timeout = aiohttp.ClientTimeout(total=timeout_s)
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "APIClient":
        self._session = aiohttp.ClientSession(
            headers=self._headers,
            timeout=self.timeout
        )
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None

    @asynccontextmanager
    async def context(self) -> AsyncIterator["APIClient"]:
        try:
            yield await self.__aenter__()
        finally:
            await self.__aexit__(None, None, None)

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path if path.startswith('/') else '/' + path}"

    async def request(
        self,
        method: HttpMethod,
        path: str,
        /,
        **kwargs
    ) -> Any:
        if self._session is None:
            raise RuntimeError(
                "APIClient no inicializado. Usa 'async with APIClient(...).context() as api:'"
            )

        # 1) Extrae timeout por petición (si viene); si no, usa el de la sesión
        timeout = kwargs.pop("timeout", self.timeout)
        if timeout is not None and not isinstance(timeout, aiohttp.ClientTimeout):
            timeout = aiohttp.ClientTimeout(total=float(timeout))

        # 2) Merge de headers
        req_headers = kwargs.pop("headers", {})
        headers = {**self._headers, **req_headers}

        # 3) Evita cuerpo de GET
        if method == "GET" and any(k in kwargs for k in ("data", "json")):
            raise ValueError("GET no debe llevar cuerpo (usa params= para query string).")

        try:
            async with self._session.request(
                method,
                self._url(path),
                headers=headers,
                timeout=timeout,
                **kwargs
            ) as response:
                response.raise_for_status()

                if response.status == 204:
                    return None  # No Content

                ctype = response.headers.get("Content-Type", "")
                if "application/json" in ctype:
                    return await response.json(content_type=None)

                text = await response.text()
                if not ctype or "text/" in ctype:
                    return text

                try:
                    return json.loads(text)
                except Exception:
                    return text

        except (asyncio.TimeoutError, aiohttp.ServerTimeoutError) as e:
            # Aquí podrías reintentar o mapear a excepción de dominio
            raise
        except aiohttp.ClientError as e:
            # Otros errores de red/HTTP (conexión, DNS, etc.)
            raise

    # Azúcares
    async def get(self, path: str, /, **kwargs) -> Any:    return await self.request("GET", path, **kwargs)
    async def post(self, path: str, /, **kwargs) -> Any:   return await self.request("POST", path, **kwargs)
    async def put(self, path: str, /, **kwargs) -> Any:    return await self.request("PUT", path, **kwargs)
    async def patch(self, path: str, /, **kwargs) -> Any:  return await self.request("PATCH", path, **kwargs)
    async def delete(self, path: str, /, **kwargs) -> Any: return await self.request("DELETE", path, **kwargs)

