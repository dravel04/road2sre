# [Amazon EKS - Knowledge Badge Readiness Path](https://explore.skillbuilder.aws/learn/lp/1931/amazon-eks-knowledge-badge-readiness-path)
Espacio para anotar los detalles que me parezcan mas importantes del curso. Ya que tengo conocimiento previo en Kubernetes, no anotaré los conceptos básicos de este.

## Test Previo
- Which AWS service can you use to troubleshoot EKS Control Plane logs? **CloudWatch Logs**
> [!NOTE] `Container Insights` summarizes metrics and logs for Containerized applications. **EKS Control Plane logs are not collected by CloudWatch container Insights**.
- **Container Isolation - Namespaces:** feature del kernel de Linux que permite limitar los procesos a los que tiene acceso otro proceso
- **Container Isolation - cgroups:** feature del kernel de Linux que permite limitar los recursos (cpu, memoria, disco I/O, network, etc) a los que tiene acceso un proceso


## Ruta de aprendizaje
- EKS despliega por ti el **control plane** que consta de 2 instancias EC2 con la API, Scheduler, etc y otras 3 instancias para `etcd`
- 


## Comentarios extra:
Algunos test tiene fallos, que he reportado a Amazon como los puntos:
- In the question, *"If you want to select the AMI of your nodes, which node group type would you select?"*, both Managed node groups and Self-managed node groups are correct answers as shown in the previous videos: "Let's go ahead and create a managed node group. I'll click on 'add node group,' and I'll call this my EC2 node group one."
- The same issue occurs in the question, "Which AMI type was built specifically for containerized workloads?" Bottlerocket is the correct answer instead of Amazon Linux 2, as demonstrated in the video: "I will choose Bottlerocket because Bottlerocket is an operating system built by Amazon specifically for containerized workloads."
