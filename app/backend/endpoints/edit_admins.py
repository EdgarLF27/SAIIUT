from flask import Blueprint, request, jsonify
import pymysql

edit_admins_bp = Blueprint('edit_admins', __name__)

# Configuración de la base de datos (ajusta según tu entorno)
db_config = {
    "host": "bfg8xigctazr1joepgzb-mysql.services.clever-cloud.com",
    "user": "uirpd1wa5zkjpk90",
    "password": "ZLaLbvvqoYAeiSErCTeM",
    "database": "bfg8xigctazr1joepgzb"
}

@edit_admins_bp.route("/editar/<int:id_admin>", methods=["PUT"])
def editar_admin(id_admin):
    data = request.json
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = """
                UPDATE admins
                SET nombre=%s, ap_P=%s, ap_M=%s, direccion=%s, telefono=%s, email=%s, sexo=%s
                WHERE id_admins=%s
            """
            cursor.execute(sql, (
                data["nombre"],
                data["ap_P"],
                data["ap_M"],
                data["direccion"],
                data["telefono"],
                data["email"],
                data["sexo"],
                id_admin
            ))
            connection.commit()
        return jsonify({"mensaje": "Admin actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()