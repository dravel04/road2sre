from flask import Flask, jsonify
import os

app = Flask(__name__)
nombre_archivo = os.path.splitext(os.path.basename(__file__))[0]

@app.route("/hello", methods=['GET'])
def hello_microservice():
	message = {"message": f"Hola desde mi primer microservicio! Esto es el ejemplo {nombre_archivo}"}
	return jsonify(message)

# Nos aseguramos de que esta linea solo se lance cuando ejecutamos el script de forma independiente
if __name__ == "__main__":
	# print(__name__)
	app.run(port=8000)
