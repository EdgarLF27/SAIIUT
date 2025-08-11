from flask import Flask
from flask_cors import CORS

from endpoints.admins import admins_bp
from endpoints.alumnos import alumnos_bp
from endpoints.profesores import profesores_bp
from endpoints.auth import auth_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(alumnos_bp, url_prefix="/alumnos")
app.register_blueprint(profesores_bp, url_prefix="/profesores")
app.register_blueprint(admins_bp, url_prefix="/admins")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
