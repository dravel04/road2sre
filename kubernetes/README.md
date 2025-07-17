# Kubernetes

La principal diferencia radica en cómo manejan los cambios en los recursos existentes:
- `kubectl create` simplemente crea un nuevo recurso o falla si el recurso ya existe.
- `kubectl apply` aplica los cambios en el recurso existente o crea uno nuevo si no existe. Es más adecuado para aplicar configuraciones en un entorno donde ya existen recursos y se necesitan actualizaciones sin afectar las partes no modificadas.

## Labels and Selectors
- **Label:**  Medatada en formato `key-value` que se añade a los recursos de declarados en kubernetes (nodos, pods, etc). Ej: `app=app1`
- **Selector:** Son los criterios con los que filtramos los recursos destinos. Ej: `kubectl get pods --selector app=app1`

Esta funcionalidad nos ayuda a asegurar que un grupo de pods corran en un nodo con concreto con [`NodeAffinity`](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
- `NodeAffinity` utiliza `Labels` en los nodos (mediante `Selectors`) para definir las reglas de afinidad. Es el mecanismo para atraer `Pods` hacia nodos con características específicas.

La diferencia con `Taints and Tolerations` es que estos te garantizan que tus pods acaben en los nodos seleccionados. Es decir, una combinación de ambos aseguran que solo los pods con la etiqueta y la tolerancia definida acaben en los nodos deseados
- Actúan como una barrera. Utilizan una lógica similar a key=value (`key=value:effect`) pero en los nodos, para repeler a los Pods que no quieres que usen el nodo, a menos que el Pod "tenga un pase" (la `Toleration`). 

> [!NOTE]
> Sólo puedes modificar las siguientes propiedades de un POD existenten, para el resto tienes que borrar y recrear el pods
> spec.containers[*].image
> spec.initContainers[*].image
> spec.activeDeadlineSeconds
> spec.tolerations

## DaemonSet
Es una definición que asegura que exista una copia del pods en **CADA UNO** de los nodos del cluster
> Por debajo, kubernetes aplica el selector `nodeSelector` con el nombre de cada node a cada pods de forma automática

## StatefulSet
Cada instancia (Pod) de la aplicación tiene una identidad persistente, un nombre de red predecible y un número ordinal único (ej., mi-app-0, mi-app-1, mi-app-2). Esta identidad se mantiene incluso si el Pod se reinicia o se reprograma en otro nodo. Las actualizaciones de los Pods de un `StatefulSet` se realizan en un orden estricto y predecible (del 0 al N-1 para escalar hacia arriba, y del N-1 al 0 para escalar hacia abajo)
> Ex: Bases de datos distribuidas, sistema de colas, etc

## Init Containers
Contenedores especiales que se ejecutan secuencialmente antes de que los contenedores principales de una aplicación se inicien. Se usan para tareas de configuración o preparación (ej., esperar por dependencias, configurar permisos, descargar archivos de configuración). Deben completarse con éxito para que el Pod principal pueda arrancar.
```yaml
# ...
# Definición de Pod (o Deployment)
spec:
  initContainers:
  - name: setup-container
    image: busybox:1.36
    command: ["sh", "-c", "echo 'Ejecutando tareas de configuración...' && sleep 5 && echo 'Configuración completada.'"]
  
  containers:
  - name: main-app-container
    image: your-app-image:latest
    # ...
```

## Networking
### Service vs Ingress
- `Service` (Capa 4 - TCP/UDP):
    + Opera a un nivel más bajo, la Capa de Transporte. Le importa la conexión directa entre direcciones IP y puertos.
    + Es ideal para cualquier tipo de tráfico que no sea necesariamente HTTP/HTTPS, como conexiones a bases de datos (MySQL, PostgreSQL), colas de mensajes (RabbitMQ, Kafka), o cualquier protocolo que use TCP o UDP.
    + Cuando expones tu base de datos con un Service (por ejemplo, tipo ClusterIP para acceso interno, o LoadBalancer si es una DB en el clúster que necesitas exponer externamente por TCP), estás operando en Capa 4. Solo te interesa que el tráfico TCP llegue al puerto correcto.

- `Ingress` (Capa 7 - HTTP/HTTPS):
    + Opera en la Capa de Aplicación, donde los detalles del protocolo HTTP/HTTPS son importantes.
    + Aquí, el Ingress puede entender y tomar decisiones de enrutamiento basándose en el contenido de la solicitud HTTP, como el nombre de host (Host), la ruta URL (Path), o incluso las cabeceras HTTP.
    + Por eso, para una aplicación web o una API REST que usa HTTP/HTTPS, un Ingress es la herramienta adecuada. Te permite tener reglas de enrutamiento inteligentes (ej., api.ejemplo.com/usuarios va a un servicio y api.ejemplo.com/productos va a otro), terminar SSL/TLS y consolidar puntos de entrada.

> `Sticky sessions`: garantizar que un usuario, una vez que ha iniciado sesión en un servidor de aplicación específico, no sea redirigido a otro servidor durante esa misma sesión. Esto es crucial para aplicaciones que mantienen un estado de usuario en memoria o que no replican el estado de sesión entre servidores
```shell
kubectl annotate ingress ingr-example \
    nginx.ingress.kubernetes.io/affinity="cookie" \
    nginx.ingress.kubernetes.io/session-cookie-name="myapp" \
    nginx.ingress.kubernetes.io/session-cookie-expires="172800"
```
Similar:
```shell
oc annotate route route-example router.openshift.io/cookie_name=myapp
```

## Storage
- `iSCSI`: Protocolo que permite el transporte de comandos SCSI (para discos) sobre una red IP estándar.
  + Proporciona **acceso a nivel de bloque (block-level storage)**.
  + Cada bloque de almacenamiento expuesto se denomina **LUN** (Logical Unit Number).
  + Una LUN es una **unidad lógica de almacenamiento** que el cliente ve como un disco duro "en blanco" o "sin formatear".
  + **El cliente es el responsable de formatear la LUN** con un sistema de archivos (ej., `ext4`, `NTFS`) y gestionarlo.
  + **La Analogía LUN - LVM (VG, PV, LV):**
    - **Discos Físicos (o particiones):** Serían los **Physical Volumes (PVs)** en LVM. Son las unidades de almacenamiento físicas subyacentes.
    - **Pool de Almacenamiento Centralizado:** Un **Volume Group (VG)** en LVM agrupa múltiples PVs (discos o particiones) para crear un gran pool de almacenamiento contiguo. Esta es la capa de abstracción del hardware, similar a una "cabina de almacenamiento" o el "software de almacenamiento definido por software" que gestiona los discos físicos.
    - **`LUN` (la unidad que se expone al servidor):** Un **Logical Volume (LV)** en LVM se crea a partir de ese VG. Un LV es un "disco virtual" que puedes formatear y usar. **Esta LV es directamente análoga a la LUN.** La LUN se "corta" de un pool de almacenamiento (como un `VG`) y se presenta a un servidor cliente vía iSCSI. La LUN abstrae la complejidad de dónde residen los datos físicamente en el pool.

### StorageClass
La `StorageClass` define los siguientes aspectos clave del almacenamiento, que son lo que permite a Kubernetes ser agnóstico al hardware de almacenamiento subyacente:
- **El `Provisioner` (El "motor" de almacenamiento):** Este es el componente más importante. El `provisioner` es un driver (generalmente un Container Storage Interface (CSI) driver) que sabe cómo interactuar con un sistema de almacenamiento específico.
    + Para **iSCSI**, la `StorageClass` apuntaría a un provisioner (por ejemplo, el driver de CSI de tu fabricante de almacenamiento, como Pure Storage o Dell EMC) que sabe cómo crear LUNs.
    + Para **NFS**, la `StorageClass` apuntaría a un provisioner de NFS.
    + El `provisioner` es el que realmente habla el protocolo de almacenamiento (iSCSI, NFS, etc.).
- **Los Parámetros (El "cómo usarlo"):** Aquí es donde la `StorageClass` te permite especificar cómo se debe crear ese almacenamiento.
    + **Tipo de filesystem:** Le dice al provisioner que formatee el volumen con `ext4` o `xfs` (en el caso de iSCSI).
    + **Modo de acceso:** Puede definir si el volumen se debe montar como `ReadWriteOnce`, `ReadOnlyMany`, etc.
    + **Nivel de rendimiento:** Algunas `StorageClass`s pueden definir un tier de rendimiento, como `ssd` o `hdd` para que el provisioner asigne el volumen desde el pool de discos adecuado.

## [Health Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- `Liveness Probe`:
    + **Objetivo**: Saber si un contenedor está vivo y funcionando correctamente.
    + **Acción si falla**: Kubernetes asume que la aplicación está en un estado irrecuperable y reinicia el contenedor.
- `Readiness Probe`:
    + **Objetivo**: Saber si un contenedor está listo para recibir tráfico.
    + **Acción si falla**: Kubernetes no envia más peticiones al Pod, es decir, retira el Pod de los `Service Endpoints`. El Pod sigue corriendo, pero aislado. Cuando vuelve a estar "ready", se añade de nuevo a los Endpoints.
- `Startup Probe`:
    + **Objetivo**: Saber si un contenedor ha terminado de iniciarse completamente.
    + **Acción si falla**: Si la sonda de inicio falla, Kubernetes reinicia el contenedor.
    + **Uso**: Para aplicaciones que tardan mucho en arrancar. Mientras `Startup Probe` está funcionando, `Liveness Probe` y `Readiness Probe` se pausan para evitar que el Pod sea reiniciado o retirado de Endpoints prematuramente. Una vez que la sonda de inicio tiene éxito, las otras dos sondas toman el control.
## [HorizontalPodAutoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
Controlador de Kubernetes que automáticamente escala el número de réplicas de un Pod (normalmente un `Deployment` o `StatefulSet`) hacia arriba o hacia abajo. Lo hace basándose en métricas de uso de recursos (como CPU o memoria) o en métricas personalizadas. Su objetivo es mantener la carga de trabajo de la aplicación dentro de los límites deseados para asegurar rendimiento y eficiencia. 

- `kubectl autoscale` (cmd: `kubectl autoscale <tipo_recurso>/<nombre_recurso> --min=<min> --max=<max> --cpu-percent=<porcentaje>`)
Comando para crear un `HPA` (Horizontal Pod Autoscaler) de forma rápida y sencilla. El `HPA` es un controlador que escala automáticamente el número de réplicas de un Pod dentro de un rango definido (mínimo y máximo), basándose en métricas (comúnmente el uso de CPU) para mantener una carga de trabajo óptima. Es una solución dinámica y reactiva a la demanda.

**Ejemplo:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: longload
  labels:
    app: longload
spec:
  maxReplicas: 3
  minReplicas: 1
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: longload
  metrics:
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 60
```
## Container Image
- `imagePullPolicy` es una configuración en el manifiesto de un recurso que crea Pods, como un Deployment, que le dice a Kubernetes cuándo debe intentar descargar una imagen de contenedor desde un registro de imágenes. Kubernetes comprueba si la imagen ya existe localmente en el nodo antes de decidir si la descarga o no, según esta política.
    + `Always`: Kubernetes siempre intentará descargar la imagen del registro, incluso si ya existe una copia local en el nodo.
        - Nota: Si el registro no está disponible o la imagen no se encuentra, el Pod no se iniciará.
    + `IfNotPresent`: Kubernetes solo descargará la imagen si no la encuentra ya en la caché local del nodo. Si la imagen ya está en el nodo, la usará sin intentar descargarla de nuevo.
    + `Never`: Kubernetes nunca intentará descargar la imagen del registro. Asume que la imagen ya está disponible localmente en el nodo.
        - **Uso:** Muy específico para entornos con imágenes pre-cargadas en los nodos (quizás para despliegues offline o de alta seguridad), o cuando se usa un image daemon local que garantiza la disponibilidad de la imagen. Si la imagen no está presente localmente, el Pod fallará al iniciarse.

## Deployments
- `oc apply` (cmd: `oc apply -f <archivo.yaml>`)
Es la forma declarativa principal de gestionar recursos. Crea el recurso si no existe, o actualiza solo las diferencias si ya lo hace, manteniendo tu YAML como la única fuente de verdad. Ideal para GitOps y automatización.

- `oc patch` (cmd: `oc patch <tipo_recurso>/<nombre_recurso> [-p PATCH|--patch-file FILE]`)
Aplica cambios específicos y puntuales a un recurso existente directamente en el clúster. No necesita el manifiesto completo, solo la porción a modificar. Útil para ajustes rápidos o scripting ad-hoc, pero no actualiza tu YAML local.

> - `--dry-run=client`: Prueba local. El comando procesa el YAML, aplica cualquier lógica predeterminada, y te muestra el objeto final que enviaría al clúster, pero nunca llega a tocar la API del clúster
> - `--dry-run=server`: El comando envía la solicitud a la API del clúster, pero le dice al servidor que no persista el recurso. El servidor realiza todas las validaciones (permisos, esquemas, existencia de otros recursos, etc.) como si fuera a crear/modificar el recurso de verdad, pero al final, descarta los cambios.

### Deployment Strategies
Una estrategia de despliegue define cómo Kubernetes (o OpenShift, que las extiende) actualiza una aplicación a una nueva versión. Dicta el orden en que los Pods antiguos se reemplazan por los nuevos, con el objetivo de minimizar o eliminar el tiempo de inactividad y gestionar el riesgo de la nueva versión.
- `RollingUpdate`: Reemplaza Pods antiguos por nuevos de forma incremental y gradual, uno por uno o en pequeños lotes.
Ofrece cero tiempo de inactividad si se configura correctamente. Es la estrategia por defecto y más común para aplicaciones de producción.
```yaml
strategy:
    type: RollingUpdate # <--- Es la predeterminada, pero se puede especificar
    rollingUpdate:
      maxUnavailable: 25% # <--- Porcentaje de Pods que pueden estar no disponibles (ej: 1 de 3)
      maxSurge: 25%       # <--- Porcentaje de Pods que pueden crearse extra (ej: 1 de 3)
```
- `Recreate`: Elimina todos los Pods antiguos y luego despliega todos los Pods de la nueva versión.
Provoca tiempo de inactividad completo de la aplicación durante la actualización.
Es la estrategia más sencilla, pero generalmente no se usa en producción.
- `Blue/Green`: Despliega la nueva versión ("Verde") completamente en paralelo a la versión actual ("Azul").
Una vez lista la "Verde", el tráfico se conmuta instantáneamente a ella.
Permite un rollback inmediato y sin interrupciones, pero duplica los recursos temporalmente.
- `Canary`: Despliega la nueva versión ("Canario") y dirige una pequeña fracción del tráfico hacia ella inicialmente.
Si es estable, el tráfico se aumenta gradualmente hasta el 100%.
Minimiza el riesgo de fallos en producción al exponer la nueva versión a pocos usuarios primero.


## Links
- [Courses roadmap](./roadmap.md)
- [Statics pods](https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/)
> Definidos en `/etc/kubernetes/manifests`
- [Multiple Scheduler](https://kubernetes.io/docs/tasks/extend-kubernetes/configure-multiple-schedulers/)
    - [Advanced Scheduling](https://kubernetes.io/blog/2017/03/advanced-scheduling-in-kubernetes/)
    - [how-does-kubernetes-scheduler-work](https://stackoverflow.com/questions/28857993/how-does-kubernetes-scheduler-work)
    - [jvns k8s Scheduler](https://jvns.ca/blog/2017/07/27/how-does-the-kubernetes-scheduler-work/)
- [CKAD Udemy](https://www.udemy.com/course/certified-kubernetes-application-developer/?couponCode=2021PM20)
- [K9s](https://k9scli.io/)
