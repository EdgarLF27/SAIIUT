import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo credentials.env
# Esto debe hacerse antes de importar cualquier módulo que las necesite.
load_dotenv("credentials.env")

# Importar el Blueprint principal de la API
from api import api_bp

app = Flask(__name__)

# Configurar la Secret Key para la sesión
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
if not app.config['SECRET_KEY']:
    raise ValueError("Error crítico: La variable de entorno SECRET_KEY no está definida en credentials.env")

# Configuración de CORS más explícita para desarrollo
CORS(app, supports_credentials=True)

# Registrar el Blueprint principal de la API
# Todas nuestras rutas ahora estarán bajo /api
app.register_blueprint(api_bp)

if __name__ == "__main__":
    # El host 0.0.0.0 hace que sea accesible desde fuera del contenedor
    app.run(host="0.0.0.0", port=5000, debug=True)