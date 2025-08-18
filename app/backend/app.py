from flask import Flask
from flask_cors import CORS

from endpoints.admins import admins_bp
from endpoints.alumnos import alumnos_bp
from endpoints.auth import auth_bp
from endpoints.profesores import profesores_bp
from endpoints.carreras import carreras_bp
from endpoints.materias import materias_bp
from endpoints.grupos import grupos_bp
from endpoints.periodos import periodos_bp
from endpoints.calificaciones import calificaciones_bp
from endpoints.tutorias import tutorias_bp
from endpoints.profesor_materias import profesor_materias_bp
from endpoints.inscripciones import inscripciones_bp
from endpoints.docente import docente_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(alumnos_bp, url_prefix="/alumnos")
app.register_blueprint(profesores_bp, url_prefix="/profesores")
app.register_blueprint(admins_bp, url_prefix="/admins")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(carreras_bp, url_prefix="/carreras")
app.register_blueprint(materias_bp, url_prefix="/materias")
app.register_blueprint(grupos_bp, url_prefix="/grupos")
app.register_blueprint(periodos_bp, url_prefix="/periodos")
app.register_blueprint(calificaciones_bp, url_prefix="/calificaciones")
app.register_blueprint(tutorias_bp, url_prefix="/tutorias")
app.register_blueprint(profesor_materias_bp)
app.register_blueprint(inscripciones_bp, url_prefix="/inscripciones")
app.register_blueprint(docente_bp, url_prefix="/docente")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)