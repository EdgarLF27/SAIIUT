from flask import Blueprint, request, jsonify
from config import get_db_connection

profesores_bp = Blueprint('profesores', __name__)

# Listar todos los profesores o filtrar si se proveen parámetros
@profesores_bp.route('/todos', methods=['GET'])
def listar_profesores():
    try:
        # Leer parámetros opcionales de la URL
        nombre = request.args.get('nombre', '')
        apellido = request.args.get('apellido', '')
        carrera = request.args.get('carrera', '')

        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM profesores"
            params = []
            conditions = []

            # Construir condiciones WHERE dinámicamente
            if nombre:
                conditions.append("(nombre LIKE %s OR ap_P LIKE %s OR ap_M LIKE %s)")
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
            profesores = cursor.fetchall()
        
        conn.close()
        return jsonify(profesores)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Buscar un profesor por ID
@profesores_bp.route('/buscar/<int:id>', methods=['GET'])
def buscar_profesor(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM profesores WHERE id_profesor=%s"
            cursor.execute(sql, (id,))
            profesor = cursor.fetchone()
        conn.close()
        if not profesor:
            return jsonify({'error': 'Profesor no encontrado'}), 404
        return jsonify(profesor)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Insertar un nuevo profesor
@profesores_bp.route('/insertar', methods=['POST'])
def insertar_profesor():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO profesores (nombre, ap_P, ap_M, no_empleado, telefono, email, sexo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data['nombre'],
                data['ap_P'],
                data['ap_M'],
                data['no_empleado'],
                data['telefono'],
                data['email'],
                data['sexo']
            ))
            conn.commit()
            profesor_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': profesor_id, **data, 'message': 'Profesor insertado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Editar un profesor existente
@profesores_bp.route('/editar/<int:id>', methods=['PUT'])
def editar_profesor(id):
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                UPDATE profesores 
                SET nombre=%s, ap_P=%s, ap_M=%s, no_empleado=%s, telefono=%s, email=%s, sexo=%s
                WHERE id_profesor=%s
            """
            cursor.execute(sql, (
                data['nombre'],
                data['ap_P'],
                data['ap_M'],
                data['no_empleado'],
                data['telefono'],
                data['email'],
                data['sexo'],
                id
            ))
            conn.commit()
            if cursor.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Profesor no encontrado'}), 404
        conn.close()
        return jsonify({'id': id, **data, 'message': 'Profesor actualizado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Eliminar un profesor por ID
@profesores_bp.route('/eliminar/<int:id>', methods=['DELETE'])
def eliminar_profesor(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "DELETE FROM profesores WHERE id_profesor=%s"
            cursor.execute(sql, (id,))
            conn.commit()
            if cursor.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Profesor no encontrado'}), 404
        conn.close()
        return jsonify({'message': 'Profesor eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    