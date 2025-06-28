from flask import Blueprint, request, jsonify
import pymysql

edit_alumnos_bp = Blueprint('edit_alumnos', __name__)

# Configuración de la base de datos (ajusta según tu entorno)
db_config = {
    "host": "bfg8xigctazr1joepgzb-mysql.services.clever-cloud.com",
    "user": "uirpd1wa5zkjpk90",
    "password": "ZLaLbvvqoYAeiSErCTeM",
    "database": "bfg8xigctazr1joepgzb"
}

@edit_alumnos_bp.route("/editar/<int:id_alumno>", methods=["PUT"])
def editar_alumno(id_alumno):
    data = request.json
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = """
                UPDATE alumnos
                SET nombre=%s, ap_P=%s, ap_M=%s, matricula=%s, telefono=%s, email=%s, carrera=%s, grado=%s, grupo=%s, sexo=%s
                WHERE id_alumno=%s
            """
            cursor.execute(sql, (
                data["nombre"],
                data["ap_P"],
                data["ap_M"],
                data["matricula"],
                data["telefono"],
                data["email"],
                data["carrera"],
                data["grado"],
                data["grupo"],
                data["sexo"],
                id_alumno
            ))
            connection.commit()
        return jsonify({"mensaje": "Alumno actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()