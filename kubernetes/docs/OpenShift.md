# OpenShift

## Adminstracion
- `oc must-gather` (cmd: `oc must-gather --dest-dir <dir>`)
Recopila una fotografía exhaustiva (logs, configs, eventos) de todo el clúster en un .tar.gz para diagnósticos profundos o soporte técnico. Es tu "todo en uno" cuando algo falla globalmente.

- `oc adm inspect` (cmd: `oc adm inspect <recurso> --dest-dir <dir> [--since <tiempo>]`)
Proporciona un diagnóstico detallado y enfocado de un recurso específico (ej., un operador o Pod) en un directorio local. Es para investigar problemas puntuales de un componente en un momento dado, ideal para depuración dirigida.

- `oc project` (cmd: `oc project <nombre_del_proyecto>` o `oc get projects`)
Comando para cambiar el proyecto (`namespace`) activo en tu sesión de CLI. También permite ver el proyecto actual o listar todos los proyectos a los que tienes acceso. Un proyecto en OpenShift es un namespace de Kubernetes con características y funcionalidades adicionales específicas de OpenShift: `RBAC` Integrado, `Quotas`, `LimitRanges`, etc

> `oc delete all` no borra recursos como `Secret` o `pvc`

### Images
- `oc image info`: (cmd: `oc image info <imagestream>:<tag>` o `oc image info <registry>/<imagen>:<tag>`)
Obtener metadatos y estado de imágenes vinculadas a `ImageStreams` o accesibles por el clúster. Útil para verificar versiones y orígenes directamente desde OpenShift

- `skopeo inspect`: (cmd: `skopeo inspect docker://<registro>/<imagen>:<tag> [--config]`)
Herramienta independiente para inspeccionar detalladamente imágenes en cualquier registro (remoto o local) sin descargarlas. Proporciona información técnica de bajo nivel (capas, config, etc.) y no requiere un clúster.

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



