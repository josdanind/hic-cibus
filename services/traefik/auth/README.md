# Configuración de `userFile` para Autenticación del Dashboard de Traefik

El archivo `userFile` se utiliza para habilitar la autenticación básica (Basic Auth) en el panel de control del dashboard de Traefik. A continuación, encontrarás las instrucciones para configurarlo correctamente.

## Pasos para Configurar el `userFile`

1. **Instalar `htpasswd`**
   Para generar las credenciales de usuario, se utiliza la herramienta `htpasswd`, que forma parte del paquete `apache2-utils` en distribuciones basadas en Debian/Ubuntu.

   ```bash
   sudo apt update
   sudo apt install apache2-utils
   ```

2. **Generar Credenciales**

   Usa `htpasswd` para crear el archivo `userFile` con credenciales de usuario.

   - Para agregar un usuario (ejemplo: admin):

      ```bash
      htpasswd -c ./userFile admin
      ```
      > **Nota:** La opción -c crea un nuevo archivo userFile. Usa esta opción solo la primera vez para evitar sobrescribir usuarios existentes.

   - Para agregar más usuarios posteriormente:

      ```bash
      htpasswd ./userFile another_user
      ```

   > **Nota:** Al ejecutar el comando, la herramienta solicitará que ingreses una contraseña para el usuario. Deberás escribirla dos veces para confirmarla.

3. **Mover el Archivo al Directorio Apropiado**

   Coloca el archivo `userFile` en la ruta esperada por Traefik, que en este caso es `./services/traefik/auth/userFile`:

   ```bash
   mv userFile ./services/traefik/auth/
   ```