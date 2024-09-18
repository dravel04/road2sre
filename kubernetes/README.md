# Kubernetes

La principal diferencia radica en cómo manejan los cambios en los recursos existentes:
- `kubectl create` simplemente crea un nuevo recurso o falla si el recurso ya existe.
- `kubectl apply` aplica los cambios en el recurso existente o crea uno nuevo si no existe. Es más adecuado para aplicar configuraciones en un entorno donde ya existen recursos y se necesitan actualizaciones sin afectar las partes no modificadas.

## Labels and Selectors
- **Label:**  Medatada en formato `key-value` que se añade a los recursos de declarados en kubernetes (nodos, pods, etc). Ej: `app=app1`
- **Selector:** Son los criterios con los que filtramos los recursos destinos. Ej: `kubectl get pods --selector app=app1`

Esta funcionalidad nos ayuda a asegurar que un grupo de pods corran en un nodo con concreto con [`NodeAffinity`](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)

La diferencia con `Taints and Tolerations` es que estos te garantizan que tus pods acaben en los nodos seleccionados. Es decir, una combinación de ambos aseguran que solo los pods con la etiqueta y la tolerancia definida acaben en los nodos deseados

> [!NOTE]
> Sólo puedes modificar las siguientes propiedades de un POD existenten, para el resto tienes que borrar y recrear el pods
> spec.containers[*].image
> spec.initContainers[*].image
> spec.activeDeadlineSeconds
> spec.tolerations

## DaemonSet
Es una definición que asegura que exista una copia del pods en **CADA UNO** de los nodos del cluster
> Por debajo, kubernetes aplica el selector `nodeSelector` con el nombre de cada node a cada pods de forma automática

## Storage


## Links
- [Statics pods](https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/)
> Definidos en `/etc/kubernetes/manifests`
- [Multiple Scheduler](https://kubernetes.io/docs/tasks/extend-kubernetes/configure-multiple-schedulers/)
    - [Advanced Scheduling](https://kubernetes.io/blog/2017/03/advanced-scheduling-in-kubernetes/)
    - [how-does-kubernetes-scheduler-work](https://stackoverflow.com/questions/28857993/how-does-kubernetes-scheduler-work)
    - [jvns k8s Scheduler](https://jvns.ca/blog/2017/07/27/how-does-the-kubernetes-scheduler-work/)
- [CKAD Udemy](https://www.udemy.com/course/certified-kubernetes-application-developer/?couponCode=2021PM20)
- [K9s](https://k9scli.io/)