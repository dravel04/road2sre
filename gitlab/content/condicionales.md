# Gitlab
## Condicionales
Se puede definir condiciones para que un job falle (o tenga éxito) utilizando varias estrategias en el archivo `.gitlab-ci.yml`. Algunas formas de manejar condiciones de fallo:
### 1. Usando el código de salida del script:
- La forma más directa de definir si un step falla es controlando el código de salida del script que se ejecuta. Cualquier código de salida distinto de `0` indica que el job ha fallado.
- Ejemplo:
```yaml
test_job:
  script:
    - ./run_tests.sh
    - if [ $? -ne 0 ]; then exit 1; fi  # Si el comando anterior falla, marca el job como fallido
```
En este ejemplo, si `./run_tests.sh` devuelve un código de salida diferente de `0`, el `exit 1` hace que el job falle.

### 2. Usando `allow_failure`:
- Si quieres que un job pueda fallar sin marcar el pipeline completo como fallido, puedes usar la opción `allow_failure: true`. Esto es útil si esperas que un step falle en ciertos casos y no quieres que eso interrumpa todo el pipeline.
- Ejemplo:
```yaml
test_job:
  script:
    - ./run_tests.sh
  allow_failure: true  # El job puede fallar, pero el pipeline continuará
```
### 3. Usando reglas (`rules`) para definir si el job debe fallar:
- Con `rules`, puedes definir condiciones específicas para ejecutar o no un job, pero también puedes usarlas para condicionar cuándo el job debe fallar o tener éxito.
- Ejemplo: Si un archivo específico no ha cambiado, no ejecutar el job.
```yaml
deploy_job:
  script:
    - ./deploy.sh
  rules:
    - changes:
        - "*.yml"  # El job solo corre si un archivo .yml ha cambiado
``` 
Si el job corre bajo ciertas condiciones y el script devuelve un código de salida distinto de 0, el job fallará automáticamente.

### 4. Usando la instrucción when para controlar el resultado:
- Puedes definir cuándo quieres que un job se considere exitoso, fallido, o manualmente aprobado mediante la instrucción when.
- Ejemplo: marcar un job para que solo falle en el caso de una condición específica.
```yaml
example_job:
  script:
    - ./run_tests.sh
  when: on_failure  # Este job solo se ejecuta si otros trabajos fallan
```
### 5. Forzando el fallo mediante un comando explícito:
- Si quieres forzar el fallo de un step bajo condiciones específicas, puedes utilizar un exit 1 directamente dentro de un comando, en combinación con lógica condicional.
- Ejemplo: fallar si un archivo no existe.
```yaml
check_file_job:
  script:
    - if [ ! -f "myfile.txt" ]; then echo "File missing!"; exit 1; fi
```