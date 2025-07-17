# Lab: Deploy Web Applications
- Create a project named `review` to store your work.
```shell
oc new-project review
```
- Configure your project so that its workloads refer to the database image by the `mysql8:1` short name.
  + The short name must point to the `registry.ocp4.example.com:8443/rhel9/mysql-80:1-228` container image. The database image name and its source registry are expected to change in the near future, and you want to isolate your workloads from that change.
  + The classroom setup copied the image from the Red Hat Ecosystem Catalog. The original image is `registry.redhat.io/rhel9/mysql-80:1-228`.
  + Ensure that the workload resources in the review project can use the `mysql8:1` resource. You create these workload resources in a later step.

``` shell
oc create is mysql8
oc create istag mysql8:1 --from-image registry.ocp4.example.com:8443/rhel9/mysql-80:1-228
```

- Create the `  ` secret to store the MySQL database parameters. Both the database and the front-end deployment need these parameters. The `dbparams` secret must include the following variables:
  - user: operator1
  - password: redhat123
  - database: quotesdb

```shell
oc create secret generic dbparams --from-literal user=operator1 --from-literal password=redhat123 --from-literal database=quotedb
```

- Create the quotesdb deployment and configure it as follows:
  + Use the `mysql8:1` image for the deployment.
  + The database must automatically roll out whenever the source container in the `mysql8:1` resource changes.
> To test your configuration, you can change the mysql8:1 image to point to the `registry.ocp4.example.com:8443/rhel9/mysql-80:1-237` container image that the classroom provides, and then verify that the quotesdb deployment rolls out. Remember to reset the `mysql8:1` image to the `registry.ocp4.example.com:8443/rhel9/mysql-80:1-228` container image before grading your work.

``` shell
# Deployment
oc create deployment quotesdb --image mysql8:1
# Trigger para auto-actualizar los pods cuando haya cambio de imagen
oc set triggers deployment/quotesdb --from-image mysql8:1 --containers mysql8
```

- Define the following environment variables in the deployment from the keys in the `dbparams` secret:
  + MYSQL_USER: user
  + MYSQL_PASSWORD: password
  + MYSQL_DATABASE: database

```shell
# Definimos las variables de entorno
oc set env deployment/quotesdb --from secret/dbparams --prefix MYSQL_
```

- Ensure that OpenShift preserves the database data between pod restarts. This data does not consume more than `2GiB` of disk space. The MySQL database stores its data under the `/var/lib/mysql` directory. Use the `lvms-vg1` storage class for the volume.

```shell
oc set volumes deployment/quotesdb --add --claim-class=lvms-vg1 --claim-size=2Gi --claim-name quotedb -m /var/lib/mysql
```

- Create a `quotesdb` service to make the database available to the front-end web application. The database service is listening on port `3306`.

```shell
oc expose deployment quotesdb --port 3306 --target-port 3306
```

- Create the `frontend` deployment and configure it as follows:
  + Use the `registry.ocp4.example.com:8443/redhattraining/famous-quotes:2-42` image. For this deployment, you refer to the image by its full name, because your organization develops the image and controls its release process.
  + Define the following environment variables in the deployment:
    - QUOTES_USER	The user key from the dbparams secret
    - QUOTES_PASSWORD	The password key from the dbparams secret
    - QUOTES_DATABASE	The database key from the dbparams secret
    - QUOTES_HOSTNAME	quotesdb

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: review
  labels:
    app: frontend
spec:
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: registry.ocp4.example.com:8443/redhattraining/famous-quotes:2-42
        env:
        - name: QUOTES_DATABASE
          valueFrom:
            secretKeyRef:
              key: database
              name: dbparams
        - name: QUOTES_PASSWORD
          valueFrom:
            secretKeyRef:
              key: password
              name: dbparams
        - name: QUOTES_USER
          valueFrom:
            secretKeyRef:
              key: user
              name: dbparams
        - name: QUOTES_HOSTNAME
          value: quotesdb
```

- The frontend deployment is listening to port `8000`.
``` shell
oc expose deployment frontend --port 8000 --target-port 8000
```

- You cannot yet test the application from outside the cluster. Expose the frontend deployment so that the application can be reached at `http://frontend-review.apps.ocp4.example.com`.

```shell
oc expose service frontend --hostname frontend-review.apps.ocp4.example.com
```

When you access the http://frontend-review.apps.ocp4.example.com URL, the application returns a list of quotations from famous authors.
