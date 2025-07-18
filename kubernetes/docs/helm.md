# Helm

Un `Chart` de Helm es el "paquete de aplicación" de Helm. Es una colección de archivos que describen un conjunto relacionado de recursos de Kubernetes. Piensa en él como una carpeta comprimida (un .tgz) que contiene:
- **Manifiestos de Kubernetes con plantillas:** Dentro de un Chart, no hay manifiestos YAML estáticos (como los que creas para oc apply). En su lugar, hay plantillas (.yaml.tpl o simplemente .yaml con sintaxis de plantillas Go) que definen los recursos de Kubernetes (Deployment, Service, Ingress, PersistentVolumeClaim, etc.). Estas plantillas tienen "huecos" o variables que se rellenan en el momento de la instalación.
- **Un archivo `values.yaml`:** Este es el corazón de la personalización. Es un archivo YAML que contiene los valores por defecto para todas las variables de tus plantillas.
- **Un archivo `Chart.yaml`:** Contiene metadatos sobre el Chart (nombre, versión, descripción, etc.).
- **Otros archivos opcionales:** Como archivos `README.md`, licencias, esquemas de valores, etc.