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
# Configuración de CORS más explícita para desarrollo
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}}, supports_credentials=True)

# Registrar el Blueprint principal de la API
# Todas nuestras rutas ahora estarán bajo /api
app.register_blueprint(api_bp)

if __name__ == "__main__":
    # El host 0.0.0.0 hace que sea accesible desde fuera del contenedor
    app.run(host="0.0.0.0", port=5000, debug=True)