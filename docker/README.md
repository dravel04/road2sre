# Docker

## Pruebas
Listado de los proyectos realizados

### [00-flask_example](./content/00-flask_example/)
Ejemplo sencillo donde tenemos dos microservicios `random` y `check`.
- `random`se encarga de generar una número aleatorio entre `(1,1000)` y lo devuelve en formato JSON
- `check` solicita un número a **random** y reporta si el número es par o impar
- Se han modificado lo servicios [originales](../python/content/microservices/) para que tenga un error `404` personalizado
- Como servidor usaremos `gunicorn` y levantaremos ambos servicios con `docker compose`
    - Los `Dockerfile` se han pensado para que hagan `multi-stage build`, donde encapsulamos python y las dependencias como `base` y el codigo de la app como `builder`
    - `compose.yml` se ha diseñado de tal forma que haga el build directamente

### TODO:
- [ ] Seguridad: Asegúrate de implementar medidas de seguridad adecuadas, como autenticación y autorización, para proteger tus endpoints y datos sensibles.
- [ ] Manejo de errores: Además de manejar el error 404, implementa un manejo de errores más completo para otros posibles errores que puedan ocurrir en tu aplicación.
- [ ] Logging: Agrega un sistema de registro (logging) para registrar eventos importantes y errores, lo que facilitará la depuración y el monitoreo de la aplicación en producción.
- [ ] Pruebas unitarias y de integración: Desarrolla pruebas automatizadas para garantizar que tu aplicación funcione correctamente y para detectar posibles problemas antes de implementarla en producción.
- [ ] Escalabilidad: Diseña tu aplicación para que pueda escalar horizontalmente fácilmente, utilizando tecnologías como balanceadores de carga y sistemas de gestión de contenedores.
- [ ] Monitorización y métricas: Implementa herramientas de monitorización y recopilación de métricas para supervisar el rendimiento de tu aplicación en producción y para identificar posibles cuellos de botella.
- [ ] Optimización de rendimiento: Realiza pruebas de rendimiento y optimiza tu código y configuración para garantizar una respuesta rápida y eficiente a las solicitudes de los clientes.
- [ ] Actualizaciones y mantenimiento: Establece un pipelines para realizar actualizaciones de forma segura y para mantener tu aplicación con las últimas correcciones de errores y mejoras.


## [01-rundeck_deploy](./content/01-rundeck_deploy/)
PoC de despliegue en contenedores de la versión comunity edition de rundeck.
### TODO:
- [ ] Usar `remco` para definir los ficheros de configuración

