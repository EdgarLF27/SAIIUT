from flask import Flask
from flask_cors import CORS
from endpoints.add_alumnos import alumnos_bp
from endpoints.add_profesores import profesores_bp  # <-- Importa el blueprint de profesores
from endpoints.add_admins import admins_bp  # <-- Importa el blueprint de admins
app = Flask(__name__)
CORS(app)

# Registrar los blueprints
app.register_blueprint(alumnos_bp, url_prefix="/alumnos")
app.register_blueprint(profesores_bp, url_prefix="/profesores")  # <-- Registra el blueprint de profesores
app.register_blueprint(admins_bp, url_prefix="/admins")  # <-- Registra el blueprint de admins

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)