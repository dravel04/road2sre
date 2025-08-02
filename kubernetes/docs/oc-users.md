## Configurar `kubeconfig`

### Configurar un `kubeconfig` para una ServiceAccount de Automatización
Este es el método recomendado para darle acceso seguro a un bot o a un pipeline de CI/CD.

1. Crea la `ServiceAccount`.
```Bash
kubectl create sa <nombre-del-bot> -n <namespace>
```

2. Define sus permisos con un `ClusterRole` (acceso global) o un `Role` (acceso por namespace).
```Bash
# Permisos en todo el clúster (por ejemplo, solo lectura de pods)
kubectl create clusterrole <rol-del-bot> --verb=get,list,watch --resource=pods
# Permisos solo en un namespace
# kubectl create role <rol-del-bot> --namespace=<namespace> --verb=get,list,watch --resource=pods
```
3. Asigna los permisos a la `ServiceAccount`.
```Bash
# Para ClusterRole
kubectl create clusterrolebinding <binding-del-bot> --clusterrole=<rol-del-bot> --serviceaccount=<namespace>:<nombre-del-bot>
# Para Role
# kubectl create rolebinding <binding-del-bot> --role=<rol-del-bot> --serviceaccount=<namespace>:<nombre-del-bot>
```
4. Obtén el token de la `ServiceAccount`.
```Bash
TOKEN=$(kubectl create token <nombre-del-bot> -n <namespace>)
```
5. Construye el archivo `kubeconfig` y guárdalo de forma segura.
```Bash
# Ejemplo de un comando que hace todo el proceso
kubectl config set-cluster $(kubectl config view --minify -o jsonpath='{.clusters[0].name}') \
  --server=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}') \
  --kubeconfig=./<nombre-del-bot>.kubeconfig && \
kubectl config set-credentials <nombre-del-bot> --token="$TOKEN" \
  --kubeconfig=./<nombre-del-bot>.kubeconfig && \
kubectl config set-context <nombre-del-bot>-context \
  --cluster=$(kubectl config view --minify -o jsonpath='{.clusters[0].name}') \
  --user=<nombre-del-bot> --namespace=<namespace> \
  --kubeconfig=./<nombre-del-bot>.kubeconfig && \
kubectl config use-context <nombre-del-bot>-context --kubeconfig=./<nombre-del-bot>.kubeconfig
```

### Crear un `kubeconfig` con un Certificado de Administrador (Puerta Trasera)
1. Creamos CSR
```bash
openssl req -newkey rsa:4096 -nodes \
  -keyout tls.key -subj "/O=backdoor-administrators/CN=admin-backdoor" \
  -out admin-backdoor-auth.csr
```
2. Generamos `CertificateSigningRequest`
```bash
cat << EOF >> admin-backdoor-csr.yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: admin-backdoor-access
spec:
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 604800  # one week
  request: $(base64 -w0 admin-backdoor-auth.csr)
  usages:
  - client auth
EOF
oc create -f admin-backdoor-csr.yaml
# Firmamos la petición
oc adm certificate approve admin-backdoor-access
```
3. Obtenemos el certificado firmado y la CA de cluster
```bash
oc get csr admin-backdoor-access -o yaml \
  | yq r - status.certificate | base64 -d > admin-backdoor-access.crt

openssl s_client -showcerts \
  -connect api.ocp4.example.com:6443 </dev/null 2>/dev/null|openssl x509 \
  -outform PEM > ocp-apiserver-cert.crt
```
4. Creamos el fichero `kubeconfig` con los privilegios del usaurio admin
```bash
oc config set-credentials admin-backdoor \
  --client-certificate admin-backdoor-access.crt --client-key tls.key \
  --embed-certs --kubeconfig admin-backdoor.config

oc config set-cluster \
  $(oc config view -o jsonpath='{.clusters[0].name}') \
  --certificate-authority ocp-apiserver-cert.crt --embed-certs=true \
  --server https://api.ocp4.example.com:6443 \
  --kubeconfig admin-backdoor.config

oc config set-context admin-backdoor \
  --cluster $(oc config view -o jsonpath='{.clusters[0].name}') \
  --namespace default --user admin-backdoor \
  --kubeconfig admin-backdoor.config

oc config use-context admin-backdoor --kubeconfig admin-backdoor.config
```

5. Validaciones finales
```bash
oc whoami --kubeconfig admin-backdoor.config
oc auth can-i create users -A --as admin-backdoor --as-group backdoor-administrators
```
