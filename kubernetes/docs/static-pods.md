# Static Pods
Un `Static Pod` es un pod que se crea directamente en un nodo sin pasar por el API Server de Kubernetes. Estos pods son gestionados por el `kubelet` (el agente en cada nodo) directamente y no por el controlador de Kubernetes.

## Características
- **Creación Manual:** Se definen directamente en los archivos de configuración del nodo, típicamente en /etc/kubernetes/manifests/. El `kubelet` en ese nodo se encarga de ejecutar y gestionar el pod.
- **No son parte del control central de Kubernetes:** Los Static Pods no son controlados por el API Server de Kubernetes. El `kubelet` los administra directamente, y aunque aparecen en el API Server, no puedes gestionarlos (reiniciar, eliminar, etc.) a través de comandos de Kubernetes como kubectl.
- **Específico del nodo:** Un Static Pod solo existe en el nodo donde el archivo de configuración está presente. No se replica automáticamente en otros nodos.
- **Casos de uso:** Se suelen usar para ejecutar componentes críticos de Kubernetes, como `etcd`, `kube-apiserver`, `kube-controller-manager`, y `kube-scheduler`. Estos componentes se ejecutan como static pods en el nodo maestro.
- **Reinicio automático:** Si el Static Pod falla, el `kubelet` lo reinicia automáticamente, ya que está siempre monitoreando esos archivos de configuración en el nodo.

### Ventajas
No depende del API Server de Kubernetes, lo cual es útil si estás ejecutando componentes que deben estar disponibles incluso cuando el API Server no lo está.
Menos overhead administrativo, ya que el `kubelet` se encarga directamente.

### Desventajas
Difícil de administrar y escalar: No puedes controlar estos pods a través de kubectl.
Sin integración con los controladores de Kubernetes, como los de autoscaling o control de replicación.
