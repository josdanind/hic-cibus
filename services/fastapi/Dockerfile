FROM python:3.12

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Actualiza pip y añade dependencias básicas
RUN pip install --no-cache-dir --upgrade pip

# Copia el código fuente al contenedor
COPY . /app/

# Instala dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt
