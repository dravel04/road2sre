# Kustomize
## base
Estructura del directorio base:
``` shell
base
├── configmap.yaml
├── deployment.yaml
├── secret.yaml
├── service.yaml
├── route.yaml
└── kustomization.yaml
```
Contenido del fichero `kustomization.yaml`:
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- configmap.yaml
- deployment.yaml
- secret.yaml
- service.yaml
- route.yaml
```

## Overlays
Un `overlay` s un archivo `kustomization.yaml` (ubicado en su propio directorio) junto con los manifiestos YAML que utiliza para modificar o añadir contenido a uno o más manifiestos base..
```shell
...
overlay
└── development
    └── kustomization.yaml
└── testing
    └── kustomization.yaml
└── production
    ├── kustomization.yaml
    └── patch.yaml
```
El fichero `overlay/producion/kustomization.yaml` incluirá:
``` yaml
kind: Kustomization
resources:
- ../../base/
patches:
- path: patch.yaml
  target:
    kind: Deployment
    name: exoplanets
```
y el `patch.yaml` solo la propiedad que queremos modificar:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: exoplanets
spec:
  replicas: 2
```

