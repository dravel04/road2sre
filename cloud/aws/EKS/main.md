# [Amazon EKS - Knowledge Badge Readiness Path](https://explore.skillbuilder.aws/learn/lp/1931/amazon-eks-knowledge-badge-readiness-path)
Espacio para anotar los detalles que me parezcan mas importantes del curso. Ya que tengo conocimiento previo en Kubernetes, no anotaré los conceptos básicos de este.

## Test Previo
- Which AWS service can you use to troubleshoot EKS Control Plane logs? **CloudWatch Logs**
> [!NOTE] `Container Insights` summarizes metrics and logs for Containerized applications. **EKS Control Plane logs are not collected by CloudWatch container Insights**.
- **Container Isolation - Namespaces:** feature del kernel de Linux que permite limitar los procesos a los que tiene acceso otro proceso
- **Container Isolation - cgroups:** feature del kernel de Linux que permite limitar los recursos (cpu, memoria, disco I/O, network, etc) a los que tiene acceso un proceso


## Ruta de aprendizaje
### Infra
- `EKS` despliega por ti el **control plane** que consta de 2 instancias EC2 con la API, Scheduler, etc y otras 3 instancias para `etcd`
- `service` solo operan en la `capa 4` manejando tráfico `TCP/UDP`. Los puertos definidos en `service` se definen a nivel de `namespace` por lo que podríamos usar el mismo número de puerto en diferentes `namespaces`
- `stateful` objeto de kubernetes pensado para aplicaciones que no pueden ser efímeras como una DB. Para garantizar la persistencia entran en juego los conceptos de `Persistent Volume Claim (pvc)` y `Persistent Volume (pv)`, el primero es la petición que hace kubernetes para solicitar un recurso de almacenamiento (local, EBS, EFS, etc) y el segundo es el recurso en sí, el volumen que montaremos en nuestro pods
- `Liveness, Readiness and Startup Probes` nos permiten configurar health checks nativos de kubernetes para verificar el estado de una aplicación a los cuales podemos añadir lógica en base a condiciones como reiniciar el pod en base a X fallos, etc
- Autenticación y autorización, funciona de la siguiente forma:
![Auth](Auth.png)
- El concepto de `ServiceAccount` en Kubernetes se utiliza principalmente para definir los permisos y la identidad de los pods dentro del clúster, es decir, para la gestión de permisos de "dentro hacia afuera". Para la asociación de permisos a usuarios externos como testers, desarrolladores, etc., se utilizan otros mecanismos de autenticación y autorización que pueden ser gestionados a nivel de `IAM (Identity and Access Management)` en la nube donde se ejecuta el clúster de Kubernetes o a través de otros sistemas de gestión de identidades.



### Aplicaciones
- Los pasos a tener en cuenta cuando queremos desplegar una app en nuestro cluster de kubernetes mediante `raw manifest` son:
    1. Definir de forma declarativa, vía yaml, los aspectos de nuestra aplicacion: qué imagen usará, cuantas replicas queremos de esta, que puerto necesita exponer, etc. Toda esta configuración estará definida en el objeto `Deployment` de kubernetes
    2. Definir el networking interno. Similar al punto anterior de forma declarativa definiremos los puertos a usar definiendo un `service`
    3. Para exponer nuestra aplicación al exterior definiremos un objecto `Ingress` en donde asociaremos diferentes path a los `services` que gestionan el tráfico de nuestra aplicación
- Otro enfoque sería crear un paquete `Helm` para nuestra aplicación
- Podemos realizar análisis de seguridad de forma estática con herramientas como [`hadolint`](https://github.com/hadolint/hadolint) o análisis en runtime con servicios como [`GuardDuty`](https://aws.amazon.com/es/guardduty/) activando `AuditLogs` en nuestro cluster EKS

## Comentarios extra:
Algunos test tiene fallos, que he reportado a Amazon como los puntos:
- In the question, *"If you want to select the AMI of your nodes, which node group type would you select?"*, both Managed node groups and Self-managed node groups are correct answers as shown in the previous videos: "Let's go ahead and create a managed node group. I'll click on 'add node group,' and I'll call this my EC2 node group one."
- The same issue occurs in the question, "Which AMI type was built specifically for containerized workloads?" Bottlerocket is the correct answer instead of Amazon Linux 2, as demonstrated in the video: "I will choose Bottlerocket because Bottlerocket is an operating system built by Amazon specifically for containerized workloads."

Algunas respuestas de los tests:
- StatefulSets make sure that Pods `Retain their name/identity` after being rescheduled.
- What is a Helm chart? `The fundamental unit used to package application resources and dependencies`
- A Kubernetes Ingress can proxy traffic to one or more Services using which of the following? `Routing rules`
- What is the hard security boundary in an Amazon EKS cluster? `The cluster`
- Which of the following integrates File Storage with Amazon EKS? `Amazon EFS CSI Driver`
- Which of the following applies to K8s secrets by default? `Encoded`
- What Amazon service was integrated with Amazon ECR to enable customers to scan container images for security vulnerabilities? `Amazon Inspector`