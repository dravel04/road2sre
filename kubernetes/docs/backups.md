# Backup y Restauración de Aplicaciones en Kubernetes**

## **1. ¿Qué es un backup en Kubernetes?**
No es solo una copia de tus datos. Es un "snapshot" completo del **estado de tu aplicación y del clúster** en un momento dado. Un backup completo incluye dos partes:
* **Recursos de la API:** Una copia de todos los manifiestos YAML (`Deployments`, `Services`, `Secrets`, `ConfigMaps`, etc.).
* **Datos de los Volúmenes:** Una copia de los datos almacenados en los `Persistent Volumes` (`PVs`).

## **2. ¿Por qué es necesario si uso IaC?**
El backup es complementario al IaC, no un reemplazo.
* **IaC:** Define la **intención** (cómo debe ser la aplicación).
* **Velero/OADP:** Restaura el **estado en vivo**, que incluye los datos, las configuraciones dinámicas y los errores humanos.

Un backup te protege de escenarios que el IaC no cubre, como la corrupción de `etcd`, la eliminación accidental de un `namespace` o la necesidad de migrar una aplicación entera a un clúster nuevo.

---

## **3. Herramientas Clave: Velero y OADP Operator**
* **Velero:** La tecnología **open source** de base. Es la herramienta que realiza el trabajo de backup, restauración y migración. Funciona en cualquier clúster de Kubernetes.
* **OADP Operator:** La solución de **Red Hat para OpenShift**. Es un operador que instala, configura y gestiona Velero de forma nativa en OpenShift. OADP usa Velero "por debajo" y simplifica su uso con una interfaz gráfica y una integración más profunda.

---

## **4. ¿Cómo y dónde se guardan los backups?**
El proceso es muy eficiente y no consume recursos del clúster:
* Los **recursos de la API** (manifiestos YAML) se guardan como un archivo comprimido en un **almacenamiento de objetos externo** (S3, MinIO, etc.).
* Los **datos de los volúmenes** se guardan como **instantáneas (`snapshots`)** en el servicio nativo del proveedor de almacenamiento.
* En entornos locales, Velero se integra con servidores S3-compatibles como MinIO y con sistemas que ofrecen un servicio de `snapshots` a través de un plugin.

---

## **5. Backup vs. Rollback**
Es una distinción crucial:
* **`Rollback`:** Revertir un cambio en el mismo clúster (a menudo no soportado en OpenShift).
* **Restauración:** Aplicar un backup a un **clúster nuevo y limpio**. Velero te permite restaurar tu aplicación a un estado funcional en un clúster de reemplazo, que es el camino correcto para recuperarse de una actualización fallida.