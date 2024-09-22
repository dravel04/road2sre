# Gitlab

## Runners
Existen diferentes [tipos de runners](https://docs.gitlab.com/runner/):
- **Self-managed:** Nos tendremos que encargar de la instalación, configuración y mantenimiento
- **GitLab-hosted:** Es la versión SaaS de estos. Alojados en la infra de Gitlab, nosotros solo seremos usuarios del resto se encargará la empresa

`Gitlab > Runner > Executor`

## Pipelines
### Rules
Podemos definir condiciones de ejecucion definiendo [`rules`](https://docs.gitlab.com/ee/ci/jobs/job_rules.html)
```yaml
job:
  script: echo "Hello, Rules!"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
      allow_failure: true
    - if: $CI_PIPELINE_SOURCE == "schedule"
```
> Dentro de estas condiciones podemos definir variables

### Services
When you configure CI/CD, you specify an image, which is used to create the container where your jobs run. To specify this image, you use the `image` keyword.

You can specify an additional image by using the [`services`](https://docs.gitlab.com/ee/ci/services/) keyword. This additional image is used to create another container, which is available to the first container. The two containers have access to one another and can communicate when running the job.

### Timeout
Podemos setear [`timeout`](https://docs.gitlab.com/ee/ci/yaml/?query=timeout) para las diferentes tareas
```yaml
build:
  script: build.sh
  timeout: 3 hours 30 minutes

test:
  script: rspec
  timeout: 3h 30m
```

### Job artifacts
Los jobs pueden tener como salida un ficheros o directorios. Este output se conoce como [`artifact`](https://docs.gitlab.com/ee/ci/jobs/job_artifacts.html) y puede ser usado por las siguientes `stages` de la pipeline

### Using variables
Existen tanto [variables por defecto](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html) como custom (globales y de job scope)
```yaml
variables:
  GLOBAL_VAR: "A global variable"

job1:
  variables: {}
  script:
    - echo This job does not need any variables
```
Como en otras herramientas podemos definir [secretos o variables privadas](https://docs.gitlab.com/ee/ci/variables/#hide-a-cicd-variable)


## Enlace de interes
- [CI/CD YAML syntax reference](https://docs.gitlab.com/ee/ci/yaml/)
- [Variables](https://docs.gitlab.com/ee/ci/variables/)
- [Resource group](https://docs.gitlab.com/ee/ci/resource_groups/)
- [Environments](https://docs.gitlab.com/ee/ci/environments/)
- [Auto DevOps](https://docs.gitlab.com/ee/topics/autodevops/)
- [Examples](https://gitlab.com/demos-group)
