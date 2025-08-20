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

### Project templates
Los **Project templates** en OpenShift permiten a los administradores definir un conjunto preconfigurado de recursos (como `Deployments`, `Services`, `Routes`, `PersistentVolumeClaims`, `Secrets`, etc.) y políticas que se aplicarán automáticamente cuando se crea un nuevo proyecto (Namespace) basado en ese template. Son una forma poderosa de estandarizar y automatizar el aprovisionamiento de entornos de aplicación completos o de proyectos con configuraciones base específicas.

Se puede generar una plantilla inicial con el siguiente comando:
```shell
oc adm create-bootstrap-project-template -o yaml > file
```
> Para que un template sea usado por defecto al lanzar `oc new-project ...` es necesario definirla en el `project` **openshift-config** y añadir el template en el campo `spec` de `projects.config.openshift.io cluster`
```yaml
...
spec:
  projectRequestTemplate:
    name: project-request
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

### Proceso de Autenticación en OpenShift con OIDC

- `oc login` te lleva al navegador para que te autentiques en tu proveedor de identidad (**IdP**). Esto es el flujo de autorización de **OAuth**.
- Una vez autenticado, el proveedor te entrega un `ID Token` y un `Refresh Token`. La entrega y validación de estos tokens es el protocolo de **OIDC**.
- Tu archivo `kubeconfig` guarda el `Refresh Token` y la configuración de **OIDC**.
- Cuando usas `kubectl`, si tu token actual ha caducado, `kubectl` usa el `Refresh Token` para conseguir uno nuevo de forma automática, sin que tengas que volver a iniciar sesión.

En resumen:
- **OAuth** maneja la redirección y el permiso.
- **OIDC** gestiona la identidad y los tokens.
- El `Refresh Token` en tu `kubeconfig` te permite mantener la sesión a largo plazo.

#### Mapeo de Usuarios con [OIDC Claims](https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims)
Los **claims de OIDC** son pares de clave-valor que el proveedor de identidad (IdP) envía a OpenShift en el ID Token. OpenShift lee estos claims para crear y gestionar los objetos de usuario, identidad y grupo del clúster.
- **Identidad del Usuario**: Debes configurar un claim para que OpenShift lo use como el identificador único del usuario. Por defecto, OpenShift usa el claim `sub` (subject identifier).
- **Detalles del Perfil**: Puedes configurar claims adicionales para obtener el nombre de usuario (`preferred_username`), el nombre completo (`name`) o el correo electrónico (`email`). OpenShift procesa estos claims en el orden que los definas y usa el primer valor que no esté vacío.

Este mapeo es lo que permite que un usuario en tu proveedor de identidad (por ejemplo, con `preferred_username: "ana.lopez"`) sea reconocido como un usuario válido en tu clúster de OpenShift.


## [Network Security](./oc-network.md)

## Limitar Workloads
Cluster Admin pueden configurar **project templates** para añadir recursos a todos los nuevos proyectos. Estos recursos pueden implementar permissions, quotas, network policies, etc

- `Requests`: Es el mínimo garantizado de CPU/Memoria que un Pod pide. Ayuda al Scheduler a encontrar un nodo. Se aplican a contenedores individuales dentro de un **Pod**.
- `Limits`: Es el máximo de CPU/Memoria que un contenedor puede usar. Si excede CPU, se limita; si excede Memoria, se termina. Se aplican a contenedores individuales dentro de un **Pod**.
- [`ResourceQuota`](https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/building_applications/quotas): Límite agregado estricto de recursos (CPU, Memoria, número de Pods/Objetos) para un único Namespace. Rechaza creaciones que superen el límite. Se aplica a un **Namespace único**
- `ClusterResourceQuota`: Límite agregado estricto de recursos para múltiples Namespaces seleccionados por etiquetas. Solo en OpenShift. Se aplica a **múltiples Namespaces** que cumplen ciertos criterios de selección (basados en etiquetas)
- `LimitRange`: Establece los valores por defecto y límites máximos/mínimos para requests y limits de contenedores/Pods dentro de un Namespace. Su objetivo es asegurar que los desarrolladores especifiquen límites razonables y evitar que desplieguen Pods sin ellos. Se aplica a un **Namespace único**.


## Seguridad
- `ServiceAccount` (SA) es la identidad que tus aplicaciones (pods) usan para interactuar con la API de Kubernetes, como un "usuario" para el software. Siempre está ligada a un **Namespace**.
- `ClusterRole` es una colección de permisos que definen qué acciones se pueden realizar sobre recursos a nivel de clúster (o sobre cualquier recurso en todos los **Namespaces**). No es una identidad, solo un listado de permisos.

Para que una **ServiceAccount** pueda usar los permisos definidos en un `ClusterRole`, necesitas un `ClusterRoleBinding`. Este objeto vincula la **ServiceAccount** (la identidad) con el **ClusterRole** (el conjunto de permisos globales), otorgándole a tu aplicación los privilegios necesarios en todo el clúster. Si los permisos son solo a nivel de **Namespace**, se usa un `Role` y un `RoleBinding`.

**Security Context Constraint (SCC)** en OpenShift es una política que controla los permisos de seguridad y las capacidades que un Pod puede tener dentro del clúster o en el host subyacente. Asegura que los contenedores operen con los privilegios mínimos necesarios.

> Si no se especifica una SA se usa la SA `default`

- `oc get <recurso>/<nombre_recurso> -o yaml | oc adm policy scc-subject-review -f -` permite evaluar qué **Security Context Constraint (SCC)** se aplicaría a los pods definidos en el manifiesto de un recurso (como un Deployment), ayudando a diagnosticar problemas de permisos o a prever cómo se ejecutarán las cargas de trabajo bajo las políticas de seguridad del clúster. No indica la SCC que el pod realmente usará si su ServiceAccount no tiene los permisos para esa SCC, es decir, hace falta asigna la política scc a la SA explicitamente (por defecto, usaran la `restricted`)

## Updates

### El Operador de Versiones del Clúster (Cluster Version Operator - CVO)

El **CVO** es el componente central que gestiona las actualizaciones del clúster. Constantemente compara el estado actual de tu clúster con un estado deseado (la nueva versión) y orquesta los cambios.
- **Basado en Operadores**: Todo en OpenShift 4.x (desde el sistema operativo base de los nodos hasta los componentes de la consola web) se gestiona como un Operador. El CVO se asegura de que todos estos Operadores se actualicen de forma coordinada.
- **Grafo de Actualizaciones**: El CVO consulta un servicio de actualización de Red Hat (OpenShift Update Service - OSUS) que proporciona un "grafo" de actualizaciones. Este grafo no solo muestra las versiones disponibles, sino también las rutas de actualización válidas y probadas para tu versión actual. Esto evita actualizaciones a versiones con problemas conocidos o rutas no soportadas.

### Canales de Actualización (Update Channels)

OpenShift ofrece diferentes canales de actualización para controlar el ritmo y la madurez de las versiones que se te ofrecen:
- **candidate-4.x**: Para los más aventureros o para pruebas tempranas. Las versiones aquí son las más recientes y pueden tener errores.
- **fast-4.x**: Versiones consideradas estables y listas para producción, liberadas tan pronto como pasan las pruebas rigurosas de Red Hat. Tienen las últimas características y correcciones.
- **stable-4.x**: Las versiones aquí tienen un período de "horneado" más largo. Son las más recomendadas para entornos de producción críticos, ya que han sido probadas extensamente en el mundo real.
- **eus-4.x (Extended Update Support)**: Canales específicos para versiones EUS que ofrecen soporte extendido por un período más largo (generalmente 24 meses), ideal para organizaciones que requieren un ciclo de actualización más lento y predecible.

Puedes cambiar el canal de actualización de tu clúster en cualquier momento desde la consola web o la CLI.

### Impacto en las Aplicaciones y "Zero Downtime"

Uno de los principales objetivos de las actualizaciones de OpenShift 4.x es lograr cero tiempo de inactividad para las aplicaciones.

- **Actualizaciones por fases**: El proceso de actualización se realiza en fases; primero el plano de control (masters y etcd), luego los nodos de control, y finalmente los nodos trabajadores y los Operadores de la plataforma.
- **Rolling Updates**: Los nodos trabajadores se actualizan de forma escalonada (rolling update). Esto significa que no todos los nodos se apagan a la vez. Los pods de tus aplicaciones se reubican a nodos ya actualizados o nodos que no están en proceso de actualización, siguiendo las mejores prácticas de Kubernetes (como PodDisruptionBudgets).
- **Operadores de Carga de Trabajo**: Si tienes Operadores de aplicaciones instalados (como para una base de datos o un middleware), el OLM (Operator Lifecycle Manager) se encarga de actualizarlos de forma segura, respetando sus capacidades de actualización.
- **Requisitos para Cero Downtime**: Para lograr un verdadero cero downtime para tus aplicaciones, tus propias aplicaciones deben estar diseñadas para alta disponibilidad (varias réplicas, PodDisruptionBudgets, etc.) y ser tolerantes a reinicios y reubicaciones de pods.


### Flujo de Actualización Típico

- **Monitoreo de la Salud**: El CVO verifica constantemente la salud del clúster y de todos los Operadores antes, durante y después de la actualización. Si algo falla, la actualización se pausará.
- **Detección de Actualizaciones**: El CVO se conecta al OpenShift Update Service y te notifica (en la consola o vía CLI) qué actualizaciones están disponibles para tu canal actual.
- **Inicio de la Actualización**: Puedes iniciar la actualización con un solo clic en la consola o con un comando `oc adm upgrade`.
- **Descarga y Verificación**: La nueva imagen de lanzamiento (que contiene todas las actualizaciones de los Operadores) se descarga y verifica su firma.
- **Orquestación de Operadores**: El CVO orquesta la actualización de los Operadores en un orden específico, desde los componentes centrales de la plataforma hasta los componentes de soporte.
- **Actualización de RHCOS**: Las imágenes de Red Hat Enterprise Linux CoreOS (RHCOS), el sistema operativo inmutable de los nodos, también se actualizan de forma automatizada. Los nodos se reinician y se inician con la nueva imagen de RHCOS.
- **Monitorización Continua**: El proceso se monitoriza continuamente, y se pausa si se detectan problemas.

----
> OpenShift **NO soporta el rollback del clúster a una versión anterior si una actualización falla o se atasca**. Si esto ocurre, debes contactar al **soporte de Red Hat**.
>
> Para tus aplicaciones, la clave es la **resiliencia**. OpenShift gestiona las actualizaciones de forma escalonada (**rolling updates**), moviendo tus pods entre nodos. Para asegurar que tus aplicaciones no sufran interrupciones (zero downtime) durante una actualización del clúster:
> - Diseña tus apps para alta disponibilidad (múltiples réplicas).
> - Usa PodDisruptionBudgets (PDBs).
> - Asegúrate de que sean tolerantes a reinicios y reubicaciones de pods.
> La responsabilidad recae en la preparación y el diseño robusto, ya que el soporte de Red Hat es la única vía si el clúster falla en una actualización.
---

### Identificación de APIs Deprecadas
`oc get apirequestcounts` nos ayuda a saber si tus aplicaciones usan APIs deprecadas en OpenShift. Busca en la columna `REMOVEDINRELEASE`, si la API está deprecada y se eliminará en esa versión de Kubernetes. Un espacio en blanco significa que no está programada para eliminación inmediata, pero podría ser deprecada más tarde. Esto te permite identificar y actualizar tus manifiestos antes de que fallen.
