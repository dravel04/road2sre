# Helm

Un `Chart` de Helm es el "paquete de aplicación" de Helm. Es una colección de archivos que describen un conjunto relacionado de recursos de Kubernetes. Piensa en él como una carpeta comprimida (un .tgz) que contiene:
- **Manifiestos de Kubernetes con plantillas:** Dentro de un Chart, no hay manifiestos YAML estáticos (como los que creas para oc apply). En su lugar, hay plantillas (.yaml.tpl o simplemente .yaml con sintaxis de plantillas Go) que definen los recursos de Kubernetes (Deployment, Service, Ingress, PersistentVolumeClaim, etc.). Estas plantillas tienen "huecos" o variables que se rellenan en el momento de la instalación.
- **Un archivo `values.yaml`:** Este es el corazón de la personalización. Es un archivo YAML que contiene los valores por defecto para todas las variables de tus plantillas.
- **Un archivo `Chart.yaml`:** Contiene metadatos sobre el Chart (nombre, versión, descripción, etc.).
- **Otros archivos opcionales:** Como archivos `README.md`, licencias, esquemas de valores, etc.

### Ver Charts
- `helm show chart <ref-chart>`: Muestra la información general (metadatos) de un Chart, como su Chart.yaml.
- `helm show values <ref-chart>`: Presenta los valores por defecto que un Chart utiliza en sus plantillas (values.yaml), útil para saber qué puedes personalizar.

### Instalar Charts
- `helm install <release> <ref-chart> -f <values.yaml>`: Crea una nueva instalación de un Chart (llamada "release") en tu clúster. Puedes personalizarla con tu propio archivo de valores.

### Inspeccionar Releases
- `helm list`: Muestra todas las instalaciones (releases) de Charts que tienes en tu clúster, incluyendo su estado y versión.
- `helm history <release>`: Consulta el historial de revisiones de una instalación específica, viendo cuándo se actualizó y qué estado tuvo cada cambio.

### Gestionar Repositorios
- `helm repo add <repo> <url-repo>`: Añade un repositorio de Charts de Helm a tu configuración local, permitiéndote buscar e instalar Charts de esa fuente.
- `helm search repo <chart>`: Busca Charts disponibles en todos los repositorios que tienes configurados localmente.
> Fichero local `~/.config/helm/repositories.yaml`
