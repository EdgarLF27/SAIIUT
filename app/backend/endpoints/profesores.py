from flask import Blueprint, request, jsonify
import pymysql

profesores_bp = Blueprint('profesores', __name__)

# Configuración de la base de datos (ajusta según tu entorno)
db_config = {
    "host": "bfg8xigctazr1joepgzb-mysql.services.clever-cloud.com",
    "user": "uirpd1wa5zkjpk90",
    "password": "ZLaLbvvqoYAeiSErCTeM",
    "database": "bfg8xigctazr1joepgzb"
}

@profesores_bp.route("/insertar", methods=["POST"])
def insertar_profesor():
    data = request.json
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO profesores
                (nombre, ap_P, ap_M, no_empleado, telefono, email, grado_estudio, sexo, id_materia, id_salon)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data["nombre"],
                data["ap_P"],
                data["ap_M"],
                data["no_empleado"],
                data["telefono"],
                data["email"],
                data["grado_estudio"],
                data["sexo"],
                data["id_materia"],
                data["id_salon"]
            ))
            connection.commit()
        return jsonify({"mensaje": "Profesor insertado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()