# Network Security
OpenShift simplifica la gestión de TLS directamente en la Route a través de los tipos de terminación:
- **edge:** El Router termina el TLS y luego el tráfico a tu Pod va sin cifrar
- **passthrough:** El Router simplemente pasa el tráfico cifrado directamente a tu Pod, donde tu aplicación se encarga de terminar el TLS
- **reencrypt:** El Router termina el TLS, luego re-cifra el tráfico y lo envía cifrado a tu Pod

Para usar esto, usaremos el comando `oc create route <terminacion> ...`. `oc expose` no te permite configurar la terminación.


## Ejemplo: Certificado autofirmado
- Generar la Clave Privada de la CA (con contraseña)
```shell
openssl genrsa -aes256 -out training-CA.key 4096
```
- Crear el Certificado Auto-Firmado de la CA:
```shell
openssl req -x509 -new -nodes -key training-CA.key -sha256 -days 3650 -out training-CA.pem
```
- Generar la Clave Privada para el Certificado del Servidor/Aplicación:
```shell
openssl genrsa -out api.key 4096
```
- Crear la Solicitud de Firma de Certificado (CSR):
```shell
openssl req -new -key api.key -out training.csr
```
- (Opcional) Crear el Fichero de Extensiones X.509 (training.ext):
```ini
# Permite que los clientes puedan verificar fácilmente que este certificado fue firmado por la CA correcta y que pueden construir la ruta de confianza hasta una CA raíz.
authorityKeyIdentifier=keyid,issuer
# Define si el certificado puede ser utilizado como una Autoridad Certificadora para firmar otros certificados.
basicConstraints=CA:FALSE 
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
# La extensión subjectAltName (SAN) en un certificado, que defines en tu 
#   fichero de extensiones como subjectAltName = @alt_names y luego en la sección
#   [alt_names], sirve precisamente para asegurar que el certificado solo sea válido 
#   para los dominios y/o IPs que has listado explícitamente allí.
subjectAltName = @alt_names
[alt_names]
DNS.1 = api.apps.acme.com
DNS.2 = my-app.acme.com
IP.1 = 192.168.1.10
```
- Firma de Certificados X.509 (openssl x509):
```shell
openssl x509 -req -in training.csr \
  -passin file:passphrase.txt \
  -CA training-CA.pem -CAkey training-CA.key -CAcreateserial \
  -out training.crt -days 1825 -sha256 -extfile training.ext
```

`service.beta.openshift.io/inject-cabundle=true` al añadir esta etique a un configMap que actue como CA, automaticamente se añade a todos los pods del cluster. (**SOLO** a nivel de namespace)
```shell
oc annotate configmap <nombre_configmap> service.beta.openshift.io/inject-cabundle=true
```

### Pasos para Configurar TLS entre Deployments en OpenShift

1.  **Configurar el Servidor TLS (Ej. stock)**
    El microservicio que va a recibir las conexiones TLS (el servidor) necesita un certificado para identificarse.
    1. **Modificar el Service del Servidor:**
        - Añade una **anotación específica de OpenShift** al `Service` de tu servidor. Esta anotación le dirá a OpenShift que genere automáticamente un **Secret TLS** que contendrá el certificado y la clave privada para este Service.
        ```yaml
        annotations:
            service.beta.openshift.io/serving-cert-secret-name: <secret_name>
        ```
    2. **Modificar el Deployment del Servidor:**
        - **Montar el Secret TLS:** Haz que el Pod de tu servidor acceda al **Secret** recién generado. Esto se hace añadiendo una sección de `volumes` y `volumeMounts` en el `Deployment`, apuntando al `Secret` creado en el paso anterior y especificando la ruta donde la aplicación esperará encontrar el certificado y la clave.
        ```yaml
        ....
        spec:
        containers:
            - name: stock
        ....
            volumeMounts:
                - name: <volume_name>
                mountPath: <>
        volumes:
            - name: <volume_name>
            secret:
                defaultMode: 420
                secretName: <secret_name>
        ```
        - **Activar TLS en la Aplicación:** Configura una **variable de entorno** en el contenedor del servidor (ej., `TLS_ENABLED`) para indicarle a tu aplicación que debe escuchar conexiones TLS.
        - **Ajustar Probes:** Si tienes sondas de salud (`livenessProbe`, `readinessProbe`), asegúrate de que ahora usen **HTTPS** en lugar de HTTP para comprobar el estado de tu aplicación.

2.  **Configurar el Cliente TLS (Ej. product)**
    El microservicio que va a iniciar las conexiones TLS (el cliente) necesita saber a dónde conectarse y cómo confiar en el certificado del servidor.
    1. **Modificar el Deployment del Cliente:**
        - **Definir la URL TLS del Servidor:** Añade una **variable de entorno** en el contenedor del cliente con la URL completa del `Service` del servidor, usando el esquema `https://`.
        - **Configurar la Confianza CA:** Añade otra **variable de entorno** que apunte a la ruta estándar del **bundle de certificados CA de confianza de OpenShift** (la CA que firmó el certificado del servidor). Opcionalmente, si el ejercicio lo pide, puedes montar explícitamente el `ConfigMap` `service-ca` en una ruta específica y apuntar a ella.
        ```yaml
        # Injectamos el configMap en en todos los pods
        apiVersion: v1
        kind: ConfigMap
        metadata:
        name: service-ca
        namespace: network-review
        annotations:
            service.beta.openshift.io/inject-cabundle: "true" # OpenShift entiende que este ConfigMap es el lugar donde debe inyectar el certificado público de su CA de servicio interna
        data: {} # aunque data este vacio, el Service CA Operator de OpenShift lo detecta y lo rellena automáticamente con el certificado de la CA que usa para firmar los certificados de servicio 
        ```

3.  **Pasos Adicionales Importantes**
    1. **Tráfico Externo al Cliente (Si aplica):**
        - Si tu microservicio cliente también es un *entry point* externo, necesitarás configurar una **Route de OpenShift** para exponerlo. Esta `Route` debe tener una **terminación TLS** configurada (como `passthrough`, `edge`, o `reencrypt`) para manejar las conexiones HTTPS entrantes.
    2. **Network Policies (Siempre recomendado):**
        - Define **Network Policies** para controlar qué Pods pueden comunicarse entre sí. Por ejemplo, una política para **stock** que solo permita conexiones desde los Pods de **product**. Utiliza **labels** para identificar los Pods y definir las reglas.