# ArgoCD

## Mapear grupos IdP con roles de ArgoCD
El bloque `sso` se encarga de la autenticación, conectando a ArgoCD con un proveedor de identidad externo como GitHub. Una vez que un usuario se autentica a través de ese proveedor, el bloque `rbac` utiliza esa información para mapear los equipos de GitHub (los grupos) a roles de permisos específicos dentro de ArgoCD. De esta forma, puedes controlar quién puede acceder a qué, basándote en la gestión de tu propia organización.

```yaml
apiVersion: argoproj.io/v1beta1
kind: ArgoCD
metadata:
  # Usa un nombre y namespace genéricos
  name: my-argocd-instance
  namespace: argo-cd
spec:
  # ... otras configuraciones de la instancia ...
  rbac:
    defaultPolicy: ""
    policy: |
      # La 'g' se refiere a un grupo que viene de tu IdP externo
      # (ej. un equipo de GitHub o un grupo de Google)
      g, your-team-name, role:admin
      g, another-team-name, role:read-only
    scopes: '[groups]'
  sso:
    dex:
      # En lugar de OpenShift, configuras un conector
      config: |
        connectors:
        - type: github
          id: github
          name: GitHub
          config:
            clientID: <tu_client_id_de_github>
            clientSecret: <el_secret_de_github>
            # Opcional: restringe el acceso a miembros de una organización específica
            orgs:
            - name: mi-organizacion-de-github
```

## Configuración de Certificados para Git

Para que ArgoCD pueda acceder a repositorios Git con **certificados HTTPS** personalizados, es necesario que el componente **`repo server`** confíe en tu certificado.

La forma de lograrlo es:
1.  Crear un **`ConfigMap`** que contenga el nuevo `bundle` de certificados que necesitas.
2.  Modificar el manifiesto de la instancia de ArgoCD para montar ese `ConfigMap` en el `path` `/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem` dentro del `pod` del **`repo server`**.
```yaml
apiVersion: argoproj.io/v1beta1
kind: ArgoCD
metadata:
  name: my-argocd-instance
  namespace: argo-cd
  ...output omitted...
spec:
  ...output omitted...
  repo:
    volumeMounts:
    - mountPath: /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
      name: volume_name
      subPath: bundle_name
    volumes:
    - configMap:
        name: configuration_map_name
      name: volume_name
...output omitted...
```
Con esto, ArgoCD reemplaza su lista de certificados de confianza por la tuya, permitiéndole comunicarse de forma segura con repositorios que usan certificados personalizados o internos.

## Configuración Certificado de la Interfaz Web de ArgoCD**

Por defecto, la instancia de ArgoCD utiliza un **certificado `self-signed`** para su interfaz web, lo que suele causar advertencias en los navegadores.

Para solucionar esto y usar un certificado de confianza, puedes configurar la `route`/`ingress` del servidor de ArgoCD con una terminación **`reencrypt`**.
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ArgoCD
metadata:
  ...output omitted...
spec:
  ...output omitted...
  server:
    ...output omitted...
    route:
      enabled: true
      tls:
        termination: reencrypt
...output omitted...
```

Esta configuración hace que el `router`/`ingress` del clúster se encargue de la conexión segura. El `router`/`ingress` utiliza su propio certificado de confianza para el tráfico entrante y luego **re-encripta** los datos antes de enviarlos al servidor de ArgoCD. De esta forma, el usuario siempre accede a la interfaz de ArgoCD a través de un certificado válido, eliminando los errores de seguridad.


Estas anotaciones de ArgoCD son fundamentales para controlar el orden y la lógica de la sincronización. Se usan para gestionar dependencias y evitar que la sincronización falle.

## Orden de despliegue
Las anotaciones `argocd.argoproj.io/sync-options` y `argocd.argoproj.io/sync-wave` controlan el comportamiento de la sincronización de ArgoCD, permitiendo una gestión más robusta de los recursos con dependencias.

- **`sync-options: SkipDryRunOnMissingResource=true`**: Le dice a ArgoCD que ignore los errores del `dry run` (ejecución de prueba) si un recurso no se encuentra en el clúster. Es útil cuando un `Deployment` hace referencia a un `Secret` que se está creando en el mismo `sync`.
- **`sync-wave: "N"`**: Permite definir un orden de despliegue. Los recursos se aplican en oleadas, de menor a mayor número. Esto garantiza que los recursos con dependencias (por ejemplo, un `Secret`) se creen antes que los que los utilizan (por ejemplo, un `Deployment`).

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
  annotations:
    argocd.argoproj.io/sync-wave: "1"
# ...
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  annotations:
    argocd.argoproj.io/sync-wave: "2"
    argocd.argoproj.io/sync-options: SkipDryRunOnMissingResource=true
spec:
  # ... usa my-secret ...
  template:
    spec:
      containers:
      - name: my-container
        envFrom:
        - secretRef:
            name: my-secret
# ...
```

## **ArgoCD Resource Hooks**

Los **`Resource Hooks`** de ArgoCD son disparadores personalizables que te permiten ejecutar acciones específicas en diferentes fases del proceso de sincronización. Son ideales para tareas que no se pueden resolver solo con la aplicación de manifiestos, como la migración de bases de datos o la ejecución de pruebas.

- **¿Cómo funcionan?** Un `hook` es cualquier recurso de Kubernetes (normalmente un `Job`) que tiene la anotación `argocd.argoproj.io/hook`.
- **Fases del `sync`**:
    + **`PreSync`**: Se ejecuta **antes** de que ArgoCD aplique los manifiestos. Es perfecto para tareas de preparación (por ejemplo, una migración de base de datos).
    + **`Sync`**: Se ejecuta **durante** la aplicación de los manifiestos.
    + **`PostSync`**: Se ejecuta **después** de que el `sync` y todos los `hooks` previos hayan tenido éxito. Ideal para tareas de verificación o pruebas de humo.
    + **`SyncFail`**: Se ejecuta **si el `sync` falla**. Útil para notificaciones o tareas de limpieza.
    + **`Skip`**: Le dice a ArgoCD que ignore un recurso durante el `sync`.
- **Limpieza automática**: La anotación `argocd.argoproj.io/hook-delete-policy` permite que ArgoCD borre el recurso del `hook` automáticamente, por ejemplo, después de que haya tenido éxito (`HookSucceeded`).

```yaml
# Ejemplo de job a ejecutar antes de la sync del proyecto
apiVersion: batch/v1
kind: Job
metadata:
  generateName: preparacion-pre-sync-
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
      - name: tarea-preparacion
        image: busybox:1.36.1 # Una imagen ligera para cualquier tarea
        command: ["/bin/sh", "-c", "echo 'Iniciando tarea de preparación...'; sleep 10; echo 'Tarea de preparación terminada con éxito!'"]
      restartPolicy: Never
```

## Rollback en ArgoCD

El `rollback` en ArgoCD te permite **revertir una aplicación a una versión anterior y estable** si un nuevo despliegue causa errores.

Puedes realizar un `rollback` de forma manual a través de la interfaz web, seleccionando una versión del historial de despliegues para restaurarla. Esto es útil para revertir rápidamente a una versión que funciona mientras preparas una solución para el problema en tu repositorio de Git.

Es importante recordar que la función de `rollback` está **desactivada si tienes la sincronización automática activada**. En este caso, ArgoCD siempre intentará volver a desplegar la última versión de Git. Para hacer un `rollback` efectivo, tienes dos opciones:
1.  **Desactivar temporalmente la sincronización automática** en ArgoCD y hacer un `rollback` manual.
2.  **Revertir el último `commit`** directamente en tu repositorio de Git.


## Argo Rollouts
**Argo Rollouts** es un controlador de Kubernetes que amplía las capacidades de despliegue estándar, permitiendo estrategias de actualización más avanzadas y seguras.

No es un reemplazo para ArgoCD, sino un complemento que se integra para darte un control granular sobre cómo se despliegan las nuevas versiones de tus aplicaciones.

- **Estrategias avanzadas**: Permite despliegues progresivos como los `canary deployments` (desplegar la nueva versión solo para un pequeño porcentaje del tráfico) o `blue-green deployments` (desplegar la nueva versión junto a la antigua y cambiar el tráfico de forma instantánea).
- **Automatización**: Puede automatizar `rollbacks` (reversiones) o `promotions` (promociones) de versiones basándose en métricas de salud y rendimiento.
- **Gestión de tráfico**: Se integra con `Ingress controllers` y `service meshes` para desviar gradualmente el tráfico entre versiones, lo que es fundamental para los `canary deployments`.


## **ArgoCD y la Consistencia Eventual**
Kubernetes opera con un modelo de "consistencia eventual", lo que significa que el estado de los recursos no es inmediato. Para gestionar esto, ArgoCD utiliza dos mecanismos:
- **Reintentos (`Retries`)**: Si un recurso no se crea correctamente al primer intento (por ejemplo, porque depende de otro que aún no existe), ArgoCD lo intentará de nuevo automáticamente.
- **Olas de Sincronización (`Sync Waves`)**: Permiten ordenar la aplicación de recursos con dependencias, asegurando que los componentes críticos se desplieguen antes que los que dependen de ellos.

## **Gestión de Datos Sensibles (Secretos) en GitOps**
Almacenar datos sensibles (como contraseñas) directamente en Git es un riesgo de seguridad. Para protegerlos, la práctica de GitOps utiliza herramientas como **`sealed secrets`** o **`external-secrets`**. Estas herramientas permiten cifrar los secretos en Git y solo el controlador en el clúster puede descifrarlos y usarlos de forma segura.

## **Server-side Apply**
El `server-side apply` es un método que permite a ArgoCD actualizar recursos existentes de manera eficiente. En lugar de sobrescribir el manifiesto completo, `server-side apply` solo aplica los cambios del manifiesto de Git, lo que reduce la posibilidad de conflictos y `overrides` de configuraciones. ArgoCD utiliza esta técnica para mantener un `diff` preciso y evitar problemas al sincronizar cambios.

En la práctica, el `server-side apply` resuelve el problema de la "lucha de controladores" en Kubernetes.

Ejemplo:
1.  **Tú, como desarrollador, creas un `Deployment`** a través de ArgoCD, donde defines que quieres `3 réplicas`.
    * `spec.replicas: 3`
2.  **El controlador de `Horizontal Pod Autoscaler` (`HPA`)**, que es otro componente de Kubernetes, está configurado para escalar tu `Deployment` si el uso de CPU sube.

**Sin `server-side apply` (El Problema)**, cuando el `HPA` detecta un pico de tráfico, cambia las réplicas de `3` a `5`. De repente, el `Deployment` que ArgoCD gestiona tiene 5 réplicas en lugar de las 3 que tú definiste en Git.

ArgoCD detecta esta diferencia y, con la lógica antigua, considera que el estado está "desincronizado". Como tu manifiesto en Git dice `replicas: 3`, ArgoCD intenta revertir el cambio y escala los `pods` de vuelta a 3. Esto crea un conflicto constante, donde el `HPA` escala y ArgoCD revierte.

- El **API Server de Kubernetes** ahora sabe que el campo `spec.replicas` es propiedad del controlador `HPA`.
- Tú, a través de tu `Deployment` en Git, sigues siendo el dueño de todos los demás campos (la imagen, los `labels`, etc.).
- Cuando ArgoCD sincroniza, ve que el campo `replicas` ha sido modificado, pero el `server-side apply` reconoce que ese campo no es de su propiedad principal, sino del `HPA`. Por lo tanto, ArgoCD **no intenta revertir el cambio del `HPA`**.

En la práctica, esto significa que el `HPA` puede escalar tu aplicación de forma dinámica sin que ArgoCD interfiera, mientras que ArgoCD sigue gestionando todos los demás campos de tu `Deployment` de forma segura. Es un sistema mucho más robusto que permite que múltiples controladores gestionen diferentes aspectos de un mismo recurso sin conflictos.

### **Cómo habilitar `server-side apply`**

Añade la siguiente anotación en el recurso `Application` de ArgoCD:
```yaml
apiVersion: argoproj.io/v1beta1
kind: Application
metadata:
  name: my-app
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-options: ServerSideApply=true
spec:
  # ... resto de la configuracion de la aplicación ...
```

De esta forma, ArgoCD usará el método más eficiente y seguro para sincronizar los recursos de tu aplicación, evitando conflictos con otros controladores de Kubernetes.

## **Multi-Instancias de ArgoCD**

1.  **Crea `namespaces` separados para cada entorno.**
```bash
# Para la instancia de desarrollo de ArgoCD
kubectl create namespace argocd-dev-instance

# Para las aplicaciones de desarrollo
kubectl create namespace app-dev-ns

# Para la instancia de producción de ArgoCD
kubectl create namespace argocd-prod-instance

# Para las aplicaciones de producción
kubectl create namespace app-prod-ns
```

2.  **Despliega las instancias de ArgoCD.**
Despliega una instancia de ArgoCD en cada uno de los `namespaces` (`argocd-dev-instance` y `argocd-prod-instance`).

3.  **Etiqueta los `namespaces` de las aplicaciones.**
Esto marca el `namespace` como propiedad de una instancia de ArgoCD específica.

```bash
# Marcar el namespace de desarrollo
kubectl label namespace app-dev-ns argocd.argoproj.io/managed-by=argocd-dev-instance

# Marcar el namespace de producción
kubectl label namespace app-prod-ns argocd.argoproj.io/managed-by=argocd-prod-instance
```

4.  **Configura los `Proyectos` de ArgoCD**
El manifiesto de `AppProject` es nativo de Kubernetes y funciona igual.
```yaml
# Proyecto para la instancia de Desarrollo
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: dev-project
  namespace: argocd-dev-instance
spec:
  sourceRepos:
  - https://git.ocp4.example.com/developer/app-dev.git
  destinations:
  - namespace: app-dev-ns
    server: https://kubernetes.default.svc
```

```yaml
# Proyecto para la instancia de Producción
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: prod-project
  namespace: argocd-prod-instance
spec:
  sourceRepos:
  - https://git.ocp4.example.com/developer/app-prod.git
  destinations:
  - namespace: app-prod-ns
    server: https://kubernetes.default.svc
```