from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import subprocess
import threading

app = Flask(__name__)
CORS(app, origins=["*"])

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    path="/api/socket.io",
    async_mode="threading"
)

@app.route('/')
def index():
    return "Servidor activo"

@socketio.on('message')
def handle_message(command):
    print(f"Comando recibido: {command}")

    def run_command():
        try:
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            socketio.emit('response', '\n')
            for line in iter(process.stdout.readline, ''):
                socketio.emit('response', line)
            process.stdout.close()
            process.wait()
            socketio.emit('response', f"\n[Proceso terminado con código {process.returncode}]\n")
        except Exception as e:
            socketio.emit('response', f"Error: {str(e)}")

    # Ejecutar el comando en un hilo aparte para no bloquear el servidor
    threading.Thread(target=run_command, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5005)
