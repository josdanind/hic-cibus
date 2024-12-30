# ⚙️ Configuración Inicial de un Droplet en DigitalOcean

## 🐳 Instalación de Docker en Ubuntu

> [🔗 Instalar Docker en Ubuntu - Documentación oficial](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script)

### 1. Actualización del sistema

```
sudo apt update && sudo apt upgrade -y
```

### 2. Actualización del sistema

Utiliza el script oficial para instalar Docker:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Verifica la instalación:

```bash
sudo docker --version
```
### 3. Configurar permisos para el usuario

#### ➡️ Agregar el usuario al grupo Docker

Esto permite que el usuario pueda ejecutar comandos Docker sin necesidad de permisos de superusuario (sudo):

```
sudo usermod -aG docker $USER
```

#### ➡️  Aplicar cambios de grupo

```
newgrp docker
```

## 🔗 Vincular Droplet con GitHub

### 1. Configurar una clave SSH

Crea una clave SSH para tu Droplet y agrégala a tu cuenta de GitHub.

#### ➡️ Generar clave SSH:

```
ssh-keygen -t ed25519 -C "tu_correo@example.com"
```

- Presiona `Enter` para aceptar la ubicación predeterminada.
- Ingresa una contraseña si lo deseas (opcional).

#### ➡️ Copiar la clave pública:

```
cat ~/.ssh/id_ed25519.pub
```

Copia el contenido y agrégalo en GitHub > Settings > SSH and GPG keys > New SSH key.

### 2. Probar la conexión SSH

Asegúrate de que el Droplet puede conectarse a GitHub:

```
ssh -T git@github.com
```

Si todo está bien, verás un mensaje como:

```
Hi username! You've successfully authenticated...
```