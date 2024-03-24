from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

@app.route("/generate", methods=['GET'])
def generate_random_number():
    random_number = random.randint(1, 1000)
    # Devolver JSON con el número aleatorio y establecer cabeceras para una respuesta exitosa
    response = jsonify({"random_number": random_number})
    return response, 200


# Ruta para manejar errores 404
@app.errorhandler(404)
def page_not_found(error):
    # Devolver un mensaje JSON con la descripción del error y establecer cabeceras para la respuesta de error 404
    response = render_template("error.html", title="Crying Cat", message="404 Not Found")

    return response, 404
