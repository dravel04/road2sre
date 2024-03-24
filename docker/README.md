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