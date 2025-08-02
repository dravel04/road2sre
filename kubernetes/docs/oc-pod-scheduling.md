# Pod Scheduling

El planificador es el proceso por el que OpenShift decide en qué nodo se ejecutará un pod

## **Ubicación de los Pods**

- **`Node Selectors`**: La forma más directa de enviar pods a un grupo específico de nodos. Puedes definirlos a nivel de pod, proyecto o clúster.
- **`Node Affinity`**: Unas reglas más flexibles que los `node selectors`. Definen si un pod **prefiere** o **requiere** ejecutarse en un grupo de nodos con ciertas etiquetas.


## **Relacionando Pods entre sí**

- **`Pod Affinity`**: Mantiene un grupo de pods **juntos**, en los mismos nodos. También pueden ser reglas **preferidas** o **requeridas**.
- **`Pod Anti-Affinity`**: Mantiene un grupo de pods **separados**, en nodos diferentes. Esto es crucial para la alta disponibilidad. También pueden ser reglas **preferidas** o **requeridas**.

## **Evitando Nodos Específicos**

- **`Taints` y `Tolerations`**: Los **`taints`** son "manchas" en los nodos que impiden que se programen pods en ellos. Un pod solo se ejecutará en un nodo con `taint` si tiene una **`toleration`** que "tolera" esa mancha. Es la herramienta principal para reservar nodos para cargas de trabajo específicas.

## **Gestión de Interrupciones**

- **`Pod Disruption Budgets` (PDBs)**: Garantizan que, durante una interrupción voluntaria (como un `rolling update`), un número mínimo de pods de una aplicación siga disponible. Esto evita que tu servicio quede inactivo.