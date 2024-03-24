# Microservicios

## Entorno
Creación de entorno virtual en python
``` shell
python3 -m venv .flask
```
Creación del fichero requirements
``` shell
cat <<EOF > .flask/requirements.txt
flask
requests
EOF
```
Activamos el venv e instalamos lo necesario
```shell
cd .flask/
source bin/activate
pip install -r requirements.txt
```
