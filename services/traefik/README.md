# Configuración de Traefik con Autenticación Básica

Este directorio contiene los archivos necesarios para configurar el servicio de Traefik, incluyendo la opción de proteger el acceso al dashboard mediante autenticación básica. Los archivos de configuración principales son `traefik.dev.toml` y `traefik.toml`.

## Generar el hash de la contraseña para `htpasswd`

Traefik utiliza un archivo llamado `htpasswd` para almacenar las credenciales con hash. A continuación, se describe el proceso para generar un hash válido y agregar usuarios.

### Generar el hash de la contraseña

En este ejemplo, se usará el usuario `admin` y la contraseña `admin`. Ejecuta el siguiente comando para generarlo:

```bash
htpasswd -nb admin admin
```

El resultado será el siguiente:

```
admin:$apr1$8ZHeV8xA$T35cRCxOMLRTR9EB5Gu0v/
```

### Crear o actualizar el archivo `htpasswd`

1. Copia la salida del comando y guárdala en un archivo llamado `htpasswd` en el directorio `/services/traefik`.

   El contenido del archivo `htpasswd` debería quedar así:

   ```
   admin:$apr1$8ZHeV8xA$T35cRCxOMLRTR9EB5Gu0v/
   ```

2. Asegúrate de que el archivo tenga los permisos adecuados:

   ```bash
   chmod 600 /services/traefik/htpasswd
   ```

Con esta guía, podrás configurar la autenticación básica para tu dashboard de Traefik utilizando el archivo `htpasswd`. Ajusta los archivos `traefik.dev.toml` y `traefik.toml` según sea necesario.
