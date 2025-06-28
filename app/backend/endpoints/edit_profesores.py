from flask import Blueprint, request, jsonify
import pymysql

edit_profesores_bp = Blueprint('edit_profesores', __name__)

# Configuración de la base de datos (ajusta según tu entorno)
db_config = {
    "host": "bfg8xigctazr1joepgzb-mysql.services.clever-cloud.com",
    "user": "uirpd1wa5zkjpk90",
    "password": "ZLaLbvvqoYAeiSErCTeM",
    "database": "bfg8xigctazr1joepgzb"
}

@edit_profesores_bp.route("/editar/<int:id_profesor>", methods=["PUT"])
def editar_profesor(id_profesor):
    data = request.json
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = """
                UPDATE profesores
                SET nombre=%s, ap_P=%s, ap_M=%s, no_empleado=%s, telefono=%s, email=%s, grado_estudio=%s, sexo=%s, id_materia=%s, id_salon=%s
                WHERE id_profesor=%s
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
                data["id_salon"],
                id_profesor
            ))
            connection.commit()
        return jsonify({"mensaje": "Profesor actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()