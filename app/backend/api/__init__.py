from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Importar y registrar cada blueprint de recurso
from .admins.routes import admins_bp
from .alumnos.routes import alumnos_bp
from .auth.routes import auth_bp
from .calificaciones.routes import calificaciones_bp
from .carreras.routes import carreras_bp
from .docente.routes import docente_bp
from .grupos.routes import grupos_bp
from .inscripciones.routes import inscripciones_bp
from .materias.routes import materias_bp
from .periodos.routes import periodos_bp
from .profesor_materias.routes import profesor_materias_bp
from .profesores.routes import profesores_bp
from .tutorias.routes import tutorias_bp
from .alumno.routes import alumno_bp

api_bp.register_blueprint(admins_bp, url_prefix='/admins')
api_bp.register_blueprint(alumnos_bp, url_prefix='/alumnos')
api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(calificaciones_bp, url_prefix='/calificaciones')
api_bp.register_blueprint(carreras_bp, url_prefix='/carreras')
api_bp.register_blueprint(docente_bp, url_prefix='/docente')
api_bp.register_blueprint(grupos_bp, url_prefix='/grupos')
api_bp.register_blueprint(inscripciones_bp, url_prefix='/inscripciones')
api_bp.register_blueprint(materias_bp, url_prefix='/materias')
api_bp.register_blueprint(periodos_bp, url_prefix='/periodos')
api_bp.register_blueprint(profesor_materias_bp) # Rutas anidadas, sin prefijo
api_bp.register_blueprint(profesores_bp, url_prefix='/profesores')
api_bp.register_blueprint(tutorias_bp, url_prefix='/tutorias')
api_bp.register_blueprint(alumno_bp, url_prefix='/alumno')