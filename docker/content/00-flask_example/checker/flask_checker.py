from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

random_microservice_url = "http://flask-random:8001/generate"

# Llamamos al microservicio que genera numeros aletorios
def call_random_microservie():
	response = requests.get(random_microservice_url)
	return response.json().get("random_number")

# Definimos el microservicio que chequea si un numero es par o impar
@app.route("/check", methods=['GET'])
def check_even_odd():
	random_number = call_random_microservie()
	result = "par" if random_number % 2 == 0 else "impar"
	response = jsonify({"random_number": random_number, "result": result})

	return response, 200


# Ruta para manejar errores 404
@app.errorhandler(404)
def page_not_found(error):
    # Devolvemos template html con gatito llorando
    response = render_template("error.html", title="Crying Cat", message="404 Not Found")

    return response, 404