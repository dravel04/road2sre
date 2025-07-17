# OpenShift

## Adminstracion
- `oc must-gather` (cmd: `oc must-gather --dest-dir <dir>`)
Recopila una fotografía exhaustiva (logs, configs, eventos) de todo el clúster en un .tar.gz para diagnósticos profundos o soporte técnico. Es tu "todo en uno" cuando algo falla globalmente.

- `oc adm inspect` (cmd: `oc adm inspect <recurso> --dest-dir <dir> [--since <tiempo>]`)
Proporciona un diagnóstico detallado y enfocado de un recurso específico (ej., un operador o Pod) en un directorio local. Es para investigar problemas puntuales de un componente en un momento dado, ideal para depuración dirigida.

- `oc project` (cmd: `oc project <nombre_del_proyecto>` o `oc get projects`)
Comando para cambiar el proyecto (`namespace`) activo en tu sesión de CLI. También permite ver el proyecto actual o listar todos los proyectos a los que tienes acceso. Un proyecto en OpenShift es un namespace de Kubernetes con características y funcionalidades adicionales específicas de OpenShift: `RBAC` Integrado, `Quotas`, `LimitRanges`, etc

> `oc delete all` no borra recursos como `Secret` o `pvc`

- `oc scale` (cmd: `oc scale <tipo_recurso>/<nombre_recurso> --replicas=<numero>`)
Comando para ajustar manualmente el número de réplicas de un recurso compatible (como un `Deployment`, `ReplicaSet` o `StatefulSet`). Es una acción directa y unívoca: estableces una cantidad fija de Pods que deseas mantener. El clúster se asegurará de que haya ese número exacto de réplicas en ejecución.



### Images
- `oc image info`: (cmd: `oc image info <imagestream>:<tag>` o `oc image info <registry>/<imagen>:<tag>`)
Obtener metadatos y estado de imágenes vinculadas a `ImageStreams` o accesibles por el clúster. Útil para verificar versiones y orígenes directamente desde OpenShift

- `skopeo inspect`: (cmd: `skopeo inspect docker://<registro>/<imagen>:<tag> [--config]`)
Herramienta independiente para inspeccionar detalladamente imágenes en cualquier registro (remoto o local) sin descargarlas. Proporciona información técnica de bajo nivel (capas, config, etc.) y no requiere un clúster.

- `ImageStream` es un registro de imágenes virtual de OpenShift que actúa como un puntero con historial, **por proyecto**. Abstrae tus despliegues del registro externo y facilita la automatización del ciclo de vida de las imágenes. Mantiene un registro de las versiones de las imágenes a lo largo del tiempo.
  +  `oc set image-lookup`: (cmd: `oc set image-lookup <nombre_imagestream> [--enabled=false]`)
  Comando para habilitar la "Política de Búsqueda Local" en un ``ImageStream`` específico. Al activarla, el `ImageStream` se vuelve descubrible por su nombre simple desde otros proyectos en el clúster. Esto facilita que otros `Deployments` (con permisos adecuados) usen imágenes de ese `ImageStream` sin necesidad de la ruta completa a su registro interno.

- `ImageStreamTag` es una referencia específica a una etiqueta (versión) dentro de un `ImageStream`. Identifica una imagen particular por su digest SHA256 y es lo que tus Deployments observan para disparar actualizaciones. Es la representación versionada de una imagen dentro del `ImageStream`.

- `oc create istag`: (cmd: `oc create istag <nombre_imagestream>:<tag_a_crear> --from-image <origen_imagen>`)
Comando para crear una nueva `ImageStreamTag` o para establecer una referencia fija e inmutable a una imagen específica de un registro externo. Si la etiqueta ya existe en el `ImageStream`, este comando fallará.

- `oc tag`: (cmd:` oc tag <origen_imagen_o_istag> <destino_imagestream>:<tag_a_actualizar> [--scheduled]`)
Comando para actualizar una `ImageStreamTag` existente de un `ImageStream`, haciendo que apunte a una nueva imagen externa o a otra `ImageStreamTag`. Es la herramienta principal para gestionar los cambios de versión de las etiquetas en un `ImageStream`, y puede configurarse con `--scheduled` para verificaciones periódicas del origen.


## Deployments
- `oc new-app` (cmd: `oc new-app <nombre_de_imagen>` o `oc new-app --template=<nombre_de_plantilla>` o `oc new-app <repositorio_git>`)
Comando para crear rápidamente aplicaciones a partir de código fuente, imágenes de contenedores existentes o plantillas (Templates). Automatiza la creación de DeploymentConfigs, Services, Routes y ImageStreams (si aplica). Es la forma más rápida de poner una aplicación en marcha en OpenShift.

- `oc process` (cmd: `oc process <nombre_de_la_plantilla> -p PARAMETRO=valor` o `oc process -f <archivo_template.yaml> -p PARAMETRO=valor`)
Comando para procesar (o renderizar) una plantilla (`Template`) existente, sustituyendo sus parámetros con valores definidos y generando el manifiesto YAML o JSON de los objetos de Kubernetes/OpenShift resultantes (ej., Pods, Deployments, Services)

## Networking
- `Route`:
Un objeto nativo de OpenShift, se integra directamente con el `OpenShift Router` (basado en `   `), que actúa como un router de Capa 7 para el tráfico HTTP y HTTPS. Su propósito es exponer servicios (`Service`) externamente al clúster, permitiendo que las aplicaciones sean accesibles desde fuera usando un nombre de host (dominio) y una ruta URL específicos. Las Routes son la implementación de OpenShift para el concepto de Ingress de Kubernetes.

- `oc expose` (cmd: `oc expose service <nombre_del_servicio>` o `oc expose deployment <nombre_del_deployment> --hostname=mi-app.ejemplo.com`)
Comando que simplifica la creación de un objeto `Route`. Su función principal es exponer una aplicación a la red externa de forma rápida y sencilla, sin necesidad de escribir manifiestos YAML complejos. Puede crear una `Route` a partir de un `Service`
  + `oc expose deployment` -> crea un `Service`
  + `oc expose service` -> crea un `Route`

- `Endpoints` (cmd: `oc get endpoints <nombre_del_servicio>` ~ `kubectl get endpoints`)
Objeto estándar de Kubernetes que representa una lista de direcciones IP y puertos de los Pods que están funcionando y son accesibles para un Service. Los `Endpoints` no se crean directamente por el usuario; son gestionados automáticamente por Kubernetes (y OpenShift) para mantener actualizado el `Service` con la información de los Pods que lo respaldan



