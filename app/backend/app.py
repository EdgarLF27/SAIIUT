from flask import Flask
from flask_cors import CORS
from endpoints.add_alumnos import alumnos_bp  # <-- Importa el blueprint de alumnos
from endpoints.add_profesores import profesores_bp  # <-- Importa el blueprint de profesores
from endpoints.add_admins import admins_bp  # <-- Importa el blueprint de admins
from endpoints.edit_admins import edit_admins_bp # <-- Importa el blueprint de edición de admins
from endpoints.edit_alumnos import edit_alumnos_bp # <-- Importa el blueprint de edición de alumnos
from endpoints.edit_profesores import edit_profesores_bp # <-- Importa el blueprint de edición de profesores
from endpoints.get_alumnos import get_alumnos_bp
app = Flask(__name__)
CORS(app)

# Registrar los blueprints
app.register_blueprint(alumnos_bp, url_prefix="/alumnos") # Registra el blueprint de alumnos
app.register_blueprint(profesores_bp, url_prefix="/profesores")  # Registra el blueprint de profesores
app.register_blueprint(admins_bp, url_prefix="/admins")  # Registra el blueprint de admins
app.register_blueprint(edit_admins_bp, url_prefix="/admins")# Registra el blueprint de edición de admins
app.register_blueprint(edit_alumnos_bp, url_prefix="/alumnos")# Registra el blueprint de edición de alumnos
app.register_blueprint(edit_profesores_bp, url_prefix="/profesores")# Registra el blueprint de edición de profesores
app.register_blueprint(get_alumnos_bp, url_prefix="/alumnos") # Registra el blueprint de obtención de alumnos

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) #Desactivar el modo debug en producción