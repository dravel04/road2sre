# Etapa 1: Construir la imagen base con Python y pip instalados
FROM python:3.9.19-alpine as base

# Instalar las dependencias globales requeridas para todas las aplicaciones
RUN pip install --no-cache-dir gunicorn flask requests

# Etapa 2: Construir la aplicación Flask
FROM base as builder

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el código de la aplicación
COPY . /app

# Expone el puerto 8001
EXPOSE 8001

# Define el comando principal que se ejecutará al iniciar el contenedor
ENTRYPOINT ["gunicorn"]

# Proporciona los argumentos adicionales para iniciar la aplicación
CMD ["--bind", "0.0.0.0:8001", "flask_checker:app"]