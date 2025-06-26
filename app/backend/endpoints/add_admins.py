from flask import Blueprint, request, jsonify
import pymysql

admins_bp = Blueprint('admins', __name__)

# Configuración de la base de datos (ajusta según tu entorno)
db_config = {
    "host": "bfg8xigctazr1joepgzb-mysql.services.clever-cloud.com",
    "user": "uirpd1wa5zkjpk90",
    "password": "ZLaLbvvqoYAeiSErCTeM",
    "database": "bfg8xigctazr1joepgzb"
}

@admins_bp.route("/insertar", methods=["POST"])
def insertar_admin():
    data = request.json
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO admins
                (nombre, ap_P, ap_M, direccion, telefono, email, sexo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data["nombre"],
                data["ap_P"],
                data["ap_M"],
                data["direccion"],
                data["telefono"],
                data["email"],
                data["sexo"]
            ))
            connection.commit()
        return jsonify({"mensaje": "Admin insertado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()