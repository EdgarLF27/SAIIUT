from flask import Flask
from endpoints.alumnos import alumnos_bp

app = Flask(__name__)

# Registrar el blueprint de alumnos
app.register_blueprint(alumnos_bp, url_prefix="/alumnos")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)