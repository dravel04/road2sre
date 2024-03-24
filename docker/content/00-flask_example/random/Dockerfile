# Usamos como imagen base una version ligera de python
FROM python:3.9.19-alpine

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el código de la aplicación al contenedor
COPY . /app

# Instala las dependencias de la aplicación
RUN pip install flask gunicorn

# Expone el puerto 8001
EXPOSE 8001

# Define el comando principal que se ejecutará al iniciar el contenedor
ENTRYPOINT ["gunicorn"]

# Proporciona los argumentos adicionales para iniciar la aplicación
CMD ["--bind", "0.0.0.0:8001", "app:app"]