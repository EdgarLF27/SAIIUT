from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

# Configuración de la base de datos (puedes usar variables de entorno)
db_config = {
    "host": "bfg8xigctazr1joepgzb-mysql.services.clever-cloud.com",
    "user": "uirpd1wa5zkjpk90",
    "password": "ZLaLbvvqoYAeiSErCTeM",
    "database": "bfg8xigctazr1joepgzb"
}

@app.route("/insertar_alumno", methods=["POST"])
def insertar_alumno():
    data = request.json
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO alumnos
                (nombre, ap_P, ap_M, matricula, telefono, email, carrera, grado, grupo, sexo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                data["sexo"]
            ))
            connection.commit()
        return jsonify({"mensaje": "Alumno insertado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)