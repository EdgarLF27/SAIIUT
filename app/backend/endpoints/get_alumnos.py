from flask import Blueprint, jsonify
import pymysql

get_alumnos_bp = Blueprint('get_alumnos', __name__)

# Configuración de la base de datos (ajusta según tu entorno)
db_config = {
    "host": "bfg8xigctazr1joepgzb-mysql.services.clever-cloud.com",
    "user": "uirpd1wa5zkjpk90",
    "password": "ZLaLbvvqoYAeiSErCTeM",
    "database": "bfg8xigctazr1joepgzb"
}

@get_alumnos_bp.route("/buscar/<int:id_alumno>", methods=["GET"])
def buscar_alumno(id_alumno):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM alumnos WHERE id_alumno=%s"
            cursor.execute(sql, (id_alumno,))
            alumno = cursor.fetchone()
        if alumno:
            return jsonify(alumno), 200
        else:
            return jsonify({"error": "Alumno no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()