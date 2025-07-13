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
