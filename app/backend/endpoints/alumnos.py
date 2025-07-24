from flask import Blueprint, request, jsonify
from config import get_db_connection

alumnos_bp = Blueprint('alumnos', __name__)

# Buscar alumnos con filtros parametrizados
@alumnos_bp.route('/todos', methods=['GET'])
def get_alumnos():
    try:
        # Leer parámetros opcionales de la URL
        nombre = request.args.get('nombre', '')
        apellido = request.args.get('apellido', '')
        carrera = request.args.get('carrera', '')

        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM alumnos"
            params = []
            conditions = []

            # Construir condiciones WHERE dinámicamente
            if nombre:
                conditions.append("(nombre LIKE %s OR ap_P LIKE %s OR ap_M LIKE %s)")
                # Buscamos el nombre en cualquiera de los campos de nombre/apellido
                search_nombre = f"%{nombre}%"
                params.extend([search_nombre, search_nombre, search_nombre])
            
            if apellido:
                conditions.append("(ap_P LIKE %s OR ap_M LIKE %s)")
                search_apellido = f"%{apellido}%"
                params.extend([search_apellido, search_apellido])

            if carrera:
                conditions.append("carrera = %s")
                params.append(carrera)

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            cursor.execute(sql, tuple(params))
            alumnos = cursor.fetchall()
        
        conn.close()
        return jsonify(alumnos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Obtener un alumno por ID  
@alumnos_bp.route('/buscar/<int:id>', methods=['GET'])
def get_alumno(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos WHERE id_alumno = %s", (id,))
            alumno = cursor.fetchone()
        conn.close()
        if alumno:
            return jsonify(alumno), 200
        else:
            return jsonify({'error': 'Alumno no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Insertar un nuevo alumno
@alumnos_bp.route('/insertar', methods=['POST'])
def create_alumno_completo():
    data = request.get_json()
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO alumnos (nombre, ap_P, ap_M, matricula, telefono, email, carrera, grado, grupo, sexo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (data['nombre'], data['ap_P'], data['ap_M'], data['matricula'], data['telefono'], data['email'], data['carrera'], data['grado'], data['grupo'], data['sexo']))
            conn.commit()
            alumno_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': alumno_id, **data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Actualizar un alumno 
@alumnos_bp.route('/editar/<int:id>', methods=['PUT'])
def update_alumno_completo(id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            UPDATE alumnos
            SET nombre=%s, ap_P=%s, ap_M=%s, matricula=%s, telefono=%s, email=%s, carrera=%s, grado=%s, grupo=%s, sexo=%s
            WHERE id_alumno=%s
            """
            cursor.execute(sql, (data['nombre'], data['ap_P'], data['ap_M'], data['matricula'], data['telefono'], data['email'], data['carrera'], data['grado'], data['grupo'], data['sexo'], id))
            conn.commit()
        conn.close()
        return jsonify({'result': 'Alumno actualizado correctamente', 'id': id, **data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Eliminar un alumno
@alumnos_bp.route('/eliminar/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM alumnos WHERE id_alumno = %s", (id,))
            conn.commit()
        conn.close()
        return jsonify({'result': 'Alumno eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



