import os
from flask import Flask
from flask_cors import CORS

# Importar el Blueprint principal de la API
from api import api_bp

app = Flask(__name__)
CORS(app)

# Registrar el Blueprint principal de la API
# Todas nuestras rutas ahora estarán bajo /api
app.register_blueprint(api_bp)

if __name__ == "__main__":
    # El host 0.0.0.0 hace que sea accesible desde fuera del contenedor
    app.run(host="0.0.0.0", port=5000, debug=True)