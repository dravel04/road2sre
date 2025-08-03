# OpenShift Observability

La observabilidad en OpenShift se divide en dos áreas principales: la **monitorización*- (métricas y alertas) y el **logging*- (registros).

## **Monitorización**

- **Propósito**: Recolectar métricas del sistema, `events` y trazas para supervisar el estado del clúster en tiempo real.
- **Base Tecnológica**: Está basada en el proyecto de código abierto **Prometheus**.
- **Implementación**: El `monitoring stack` por defecto viene incluido con OpenShift y se instala en el `namespace` `openshift-monitoring`.
- **Alertas**:
    - **Reglas de Alerta**: Definen las condiciones que, si se cumplen, activan una alerta.
    - **Alerta**: Se dispara cuando las condiciones de una regla son ciertas.
    - **Silencio (`Silence`)**: Permite desactivar temporalmente las notificaciones de una alerta.

### **Componentes del Stack de Monitorización por Defecto**

El `stack` de monitorización de OpenShift está diseñado para ser gestionado por operadores. Es fundamental no modificar sus recursos directamente en el `namespace` `openshift-monitoring`, ya que el `stack` los restaurará automáticamente.

- **Cluster Monitoring Operator**: El cerebro central. Este operador se asegura de que todos los demás componentes de monitorización estén siempre al día y en el estado esperado.
- **Prometheus Operator**: Despliega y configura Prometheus y Alertmanager, que son los componentes clave para métricas y alertas.
- **Prometheus**: El servidor de monitorización. Se encarga de recolectar las métricas de todos los componentes del clúster.
    - **PromQL**: El lenguaje de consulta de Prometheus. Te permite buscar, filtrar y agregar las métricas recolectadas. Por ejemplo, una consulta como `sum(rate(container_cpu_usage_seconds_total[5m]))` te daría el uso promedio de CPU.
- **Prometheus Alertmanager**: El gestor de alertas. Recibe las alertas de Prometheus y las agrupa para enviarlas a destinos específicos.
    - **Alertas y Notificaciones**: Las alertas no se envían a ningún sistema de notificación por defecto. Debes configurar Alertmanager para que envíe las notificaciones a destinos como **Email, PagerDuty, Slack, o un `Webhook`**.
    - **Configuración de Alertmanager**: La configuración de Alertmanager se almacena en el `Secret` `alertmanager-main` dentro del `namespace` `openshift-monitoring`.
- **Prometheus Adapter**: Permite que las métricas de Prometheus se usen para escalar `pods` automáticamente (Horizontal Pod Autoscaling o HPA).
- **Kube y OpenShift State Metrics**: Son agentes que convierten los objetos de Kubernetes y de OpenShift en métricas que Prometheus puede entender.
- **Node Exporter**: Un agente que exporta métricas de bajo nivel de los nodos del clúster.
- **Thanos Querier**: Una interfaz para consultar métricas de Prometheus de forma agregada, deduplicada y multitenant.
- **Telemeter Client**: Envía métricas del estado del clúster a Red Hat para un monitoreo remoto.
- **Consola Web (`Observe`)**: Es la interfaz gráfica de la consola de OpenShift donde puedes ver todos los `dashboards`, métricas y alertas.


## **Logging**
El `stack` de logging de OpenShift agrega los `logs` de todos los `pods` y nodos en una ubicación centralizada.

- **Implementación**: El **OpenShift Logging Operator** gestiona el `stack` de `logging` a través del `CRD ClusterLogging`.
- **Componentes Clave**:
    - **Collector**: Un componente como **Vector** (o antes Fluentd) que recoge los `logs` de todos los contenedores y nodos.
    - **Log Store**: El almacén de `logs`. Desde OpenShift 4.10, la opción por defecto es **Grafana Loki**. Antes se usaba **Elasticsearch**. **Loki** es un sistema más ligero que indexa los `logs` basándose en etiquetas, no en su contenido completo.
    - **Visualization**: Una consola (`UI`) para visualizar y consultar los `logs`.
- **Características Adicionales**:
    - **Lenguaje de Consulta**: **Loki** utiliza **LogQL** como lenguaje de consulta.
    - **Log Forwarding**: Permite reenviar `logs` a un sistema externo.
    - **Audit Logs**: Requiere configuración manual a través de un `log forwarder`.
    - **Event Router**: Un componente opcional que registra los `Kubernetes events`.


## Rastreo Distribuido (`Tracing`)

El rastreo es fundamental para diagnosticar problemas de rendimiento o errores en arquitecturas de microservicios.

- **Propósito**: Permite seguir el flujo de una única petición a medida que viaja por los distintos servicios de una aplicación. Ayuda a identificar dónde se produce un retraso o un fallo en la cadena de comunicación.
- **Base Tecnológica**: OpenShift utiliza el proyecto **Jaeger*- como `backend` para el rastreo.
- **Implementación**: La plataforma de `tracing` distribuido de Red Hat se instala a través de un operador que gestiona los componentes necesarios para recolectar, almacenar y visualizar los rastros.
- **Funcionamiento**: Para usar el rastreo, es necesario que las aplicaciones se instrumenten con bibliotecas que generen `traces` y las envíen a un colector de Jaeger.
