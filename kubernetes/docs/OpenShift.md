# OpenShift

## Adminstracion
- **`oc must-gather` (cmd:** `oc must-gather --dest-dir <dir>`)
Recopila una fotografía exhaustiva (logs, configs, eventos) de todo el clúster en un .tar.gz para diagnósticos profundos o soporte técnico. Es tu "todo en uno" cuando algo falla globalmente.

- **`oc adm inspect` (cmd:** `oc adm inspect <recurso> --dest-dir <dir> [--since <tiempo>]`)
Proporciona un diagnóstico detallado y enfocado de un recurso específico (ej., un operador o Pod) en un directorio local. Es para investigar problemas puntuales de un componente en un momento dado, ideal para depuración dirigida.

- **`oc project` (cmd:** `oc project <nombre_del_proyecto>` o `oc get projects`)
Comando para cambiar el proyecto (`namespace`) activo en tu sesión de CLI. También permite ver el proyecto actual o listar todos los proyectos a los que tienes acceso. Un proyecto en OpenShift es un namespace de Kubernetes con características y fu**ncionalidades adicionales específicas de OpenShift:** `RBAC` Integrado, `Quotas`, `LimitRanges`, etc

> `oc delete all` no borra recursos como `Secret` o `pvc`

- **`oc scale` (cmd:** `oc scale <tipo_recurso>/<nombre_recurso> --replicas=<numero>`)
Comando para ajustar manualmente el número de réplicas de un recurso compatible (como un `Deployment`, `ReplicaSet` o `S**tatefulSet`). Es una acción directa y unívoca:** estableces una cantidad fija de Pods que deseas mantener. El clúster se asegurará de que haya ese número exacto de réplicas en ejecución.

- **`oc diff` (cmd:** `oc diff -f <archivo.yaml>`)
Comando para mostrar las diferencias entre el estado actual de un recurso en el clúster y el estado deseado definido en un archivo YAML local. Te permite previsualizar los cambios que se aplicarían sin modificar realmente el recurso en el clúster. Es una herramienta esencial para revisar y validar las modificaciones antes de ejecutarlas con `oc apply` o `oc replace`.

### Images
- **`oc image info`: (cmd: `oc image info <imagestream>:<tag>` o `oc image info <registry>/<imagen>:**<tag>`)
Obtener metadatos y estado de imágenes vinculadas a `ImageStreams` o accesibles por el clúster. Útil para verificar versiones y orígenes directamente desde OpenShift

- **`skopeo inspect`: (cmd: `skopeo inspect docker://<registro>/<imagen>:**<tag> [--config]`)
Herramienta independiente para inspeccionar detalladamente imágenes en cualquier registro (remoto o local) sin descargarlas. Proporciona información técnica de bajo nivel (capas, config, etc.) y no requiere un clúster.

- `ImageStream` es un registro de imágenes virtual de OpenShift que actúa como un puntero con historial, **por proyecto**. Abstrae tus despliegues del registro externo y facilita la automatización del ciclo de vida de las imágenes. Mantiene un registro de las versiones de las imágenes a lo largo del tiempo.
  + **`oc set image-lookup`**: (cmd:** `oc set image-lookup <nombre_imagestream> [--enabled=false]`)
  Comando para habilitar la "Política de Búsqueda Local" en un ``ImageStream`` específico. Al activarla, el `ImageStream` se vuelve descubrible por su nombre simple desde otros proyectos en el clúster. Esto facilita que otros `Deployments` (con permisos adecuados) usen imágenes de ese `ImageStream` sin necesidad de la ruta completa a su registro interno.

- `ImageStreamTag` es una referencia específica a una etiqueta (versión) dentro de un `ImageStream`. Identifica una imagen particular por su digest SHA256 y es lo que tus Deployments observan para disparar actualizaciones. Es la representación versionada de una imagen dentro del `ImageStream`.

- **`oc create istag`**: (cmd: `oc create istag <nombre_imagestream>:**<tag_a_crear> --from-image <origen_imagen>`)
Comando para crear una nueva `ImageStreamTag` o para establecer una referencia fija e inmutable a una imagen específica de un registro externo. Si la etiqueta ya existe en el `ImageStream`, este comando fallará.

- **`oc tag`**: (cmd:` oc tag <origen_imagen_o_istag> <destino_imagestream>:**<tag_a_actualizar> [--scheduled]`)
Comando para actualizar una `ImageStreamTag` existente de un `ImageStream`, haciendo que apunte a una nueva imagen externa o a otra `ImageStreamTag`. Es la herramienta principal para gestionar los cambios de versión de las etiquetas en un `ImageStream`, y puede configurarse con `--scheduled` para verificaciones periódicas del origen.


## Deployments
- **`oc new-app` (cmd:** `oc new-app <nombre_de_imagen>` o `oc new-app --template=<nombre_de_plantilla>` o `oc new-app <repositorio_git>`)
Comando para crear rápidamente aplicaciones a partir de código fuente, imágenes de contenedores existentes o plantillas (Templates). Automatiza la creación de DeploymentConfigs, Services, Routes y ImageStreams (si aplica). Es la forma más rápida de poner una aplicación en marcha en OpenShift.

- **`oc process` (cmd:** `oc process <nombre_de_la_plantilla> -p PARAMETRO=valor` o `oc process -f <archivo_template.yaml> -p PARAMETRO=valor`)
Comando para procesar (o renderizar) una plantilla (`Template`) existente, sustituyendo sus parámetros con valores definidos y generando el manifiesto YAML o JSON de los objetos de Kubernetes/OpenShift resultantes (ej., Pods, Deployments, Services)

## Networking
- **`Route`:**
Un objeto nativo de OpenShift, se integra directamente con el `OpenShift Router` (basado en `HAProxy`), que actúa como un router de Capa 7 para el tráfico HTTP y HTTPS. Su propósito es exponer servicios (`Service`) externamente al clúster, permitiendo que las aplicaciones sean accesibles desde fuera usando un nombre de host (dominio) y una ruta URL específicos. Las Routes son la implementación de OpenShift para el concepto de Ingress de Kubernetes.

- **`oc expose` (cmd:** `oc expose service <nombre_del_servicio>` o `oc expose deployment <nombre_del_deployment> --hostname=mi-app.ejemplo.com`)
Comando que simplifica la creación de un objeto `Route`. Su función principal es exponer una aplicación a la red externa de forma rápida y sencilla, sin necesidad de escribir manifiestos YAML complejos. Puede crear una `Route` a partir de un `Service`
  + `oc expose deployment` -> crea un `Service`
  + `oc expose service` -> crea un `Route`

- **Service Type LoadBalancer**: Este tipo de Service expone tu aplicación de forma externa al provisionar automáticamente un balanceador de carga dedicado. Asigna una IP pública estable que distribuye el tráfico entrante a los Pods de tu aplicación, eliminando la gestión manual de reglas de red o la alta disponibilidad. Es distinto de las Routes de OpenShift, que añaden funcionalidades específicas como la terminación TLS avanzada o el virtual hosting.
  + `oc expose deployment <nombre-deployment> --port=<puerto-externo> --target-port=<puerto-interno> --type=LoadBalancer [--name=<nombre-service>]`

- **`Endpoints` (cmd:** `oc get endpoints <nombre_del_servicio>` ~ `kubectl get endpoints`)
Objeto estándar de Kubernetes que representa una lista de direcciones IP y puertos de los Pods que están funcionando y son accesibles para un Service. Los `Endpoints` no se crean directamente por el usuario; son gestionados automáticamente por Kubernetes (y OpenShift) para mantener actualizado el `Service` con la información de los Pods que lo respaldan

### Uso diferentes Networks
Permite que un Pod tenga más de una interfaz de red, cada una conectada a una red lógica o física diferente. La red principal se obtiene del CNI del clúster (por defecto), y las redes adicionales se configuran mediante recursos como `NetworkAttachmentDefinition` y un plugin CNI como **Multus**.
- **Propósito**: No se trata de dar acceso "directo" al Pod fuera del clúster (eso lo hacen Services tipo LoadBalancer/NodePort o Ingress/Route). Su objetivo es:
  - **Separar el tráfico**: Por ejemplo, una interfaz para tráfico de aplicación y otra para gestión, almacenamiento o monitorización.
  - **Mejorar el rendimiento**: Conectar a redes de alto rendimiento o usar tecnologías como SR-IOV.
  - **Aislamiento/Seguridad**: Aplicar políticas de red distintas a cada interfaz.

```yaml
# Añadiriamos al deployment tras crear el NetworkAttachmentDefinition
annotations:
  k8s.v1.cni.cncf.io/networks: <red1_NAD_nombre>,<red2_NAD_nombre>
```


**Cuándo es útil**: En escenarios avanzados donde la red única del Pod no es suficiente para las necesidades de rendimiento, seguridad o segregación de tráfico de aplicaciones muy específicas (ej., bases de datos, aplicaciones de red intensivas, telecomunicaciones).

## Templates
Los `OpenShift Templates` son una forma de empaquetar y personalizar conjuntos de manifiestos YAML (`Deployment`, `Service`, `Route`, etc.) para su fácil despliegue. Funcionan como plantillas que usan parámetros (parameters) que el usuario rellena al momento de procesarlos con oc process. Son una característica específica de OpenShift, ideal para desplegar aplicaciones preconfiguradas o para simplificar la creación de recursos complejos a usuarios con menos experiencia.

> Las variables dentro del yaml se definen como en bash `${VAR_NAME}`

```shell
# 1. Registras el manifiesto del template
oc create -f <roster-template path .yaml>
# 2. Lo usas para desplegar apps
oc process roster-template -p MYSQL_USER=user1 -p MYSQL_PASSWORD=mypasswd -p INIT_DB=true | oc apply -f -

cat roster-parameters.env <<EOF
MYSQL_USER=user1
MYSQL_PASSWORD=mypasswd
IM**AGE=registry.ocp4.example.com:8443/redhattraining/do280-roster:**v2
EOF
oc process roster-template --param-file=roster-parameters.env | oc apply -f -

# ?. Puedes revisar los cambios antes de aplicarlos
oc process roster-template --param-file=roster-parameters.env | oc diff -f -
```

## Authentication and Authorization

### Usuarios y Grupos en OpenShift
- **User:** Representa a un individuo o actor que interactúa con el servidor API. Los permisos se asignan a ellos directamente o mediante grupos. (se crean automaticos al logar existosamente)
- **Identity:** Registra los intentos de autenticación exitosos de un usuario desde un proveedor de identidad (como OAuth). Contiene información sobre el origen de la autenticación. (se crean automaticos al logar existosamente)
- **Service Account:** Una identidad para aplicaciones o procesos automáticos, no para personas. Permite a las apps interactuar con el API sin usar credenciales de usuario regulares, manteniendo la seguridad.
- **Group:** Una colección de usuarios. Se usan para asignar permisos a múltiples usuarios a la vez mediante roles, simplificando la gestión de accesos. OpenShift también tiene grupos de sistema automáticos.
- **Role:** Define las operaciones (permisos) que un usuario, grupo o Service Account puede realizar sobre tipos de recursos específicos en el API. Se asignan para otorgar esos permisos.

#### Flujo de Uso de Service Accounts (SA) en OpenShift/Kubernetes

1. Crear SA: Define la identidad de tu aplicación (solo nombre y namespace).
```shell
kubectl create serviceaccount <nombre-sa> -n <namespace>
```
2. Crear Role: Define los permisos específicos (qué acciones sobre qué recursos).
```shell
kubectl create role <nombre-role> -n <namespace> --verb=<verbo> --resource=<recurso> (o desde un archivo YAML)
```
3. Asociar Role con SA (RoleBinding): Vincula la SA al Role para otorgarle los permisos definidos.
```shell
kubectl create rolebinding <nombre-rb> --role=<nombre-role> --serviceaccount=<namespace>:<nombre-sa> -n <namespace> (o desde un archivo YAML)
```
4. Usar la SA: Asigna la SA al Pod o Deployment para que tu aplicación herede esos permisos. En el YAML del Pod/Deployment: `spec.template.spec.serviceAccountName: <nombre-sa>`

## [Network Security](./oc-network.md)


