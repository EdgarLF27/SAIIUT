from flask import Flask
from flask_cors import CORS
from endpoints.alumnos import alumnos_bp
from endpoints.profesores import profesores_bp  # <-- Importa el blueprint de profesores

app = Flask(__name__)
CORS(app)

# Registrar los blueprints
app.register_blueprint(alumnos_bp, url_prefix="/alumnos")
app.register_blueprint(profesores_bp, url_prefix="/profesores")  # <-- Registra el blueprint de profesores

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)