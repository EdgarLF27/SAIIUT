from flask import Blueprint, request, jsonify
from config import get_db_connection

admins_bp = Blueprint('admins', __name__)

# Obtener todos los admins
@admins_bp.route('/todos', methods=['GET'])
def get_admins():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_admins, nombre, ap_P, ap_M, direccion, telefono, email, sexo FROM admins")
            admins = cursor.fetchall()
        conn.close()
        return jsonify(admins), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Obtener un admin por ID
@admins_bp.route('/buscar/<int:id>', methods=['GET'])
def get_admin(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM admins WHERE id_admins = %s", 
                (id,)
            )
            admin = cursor.fetchone()
        conn.close()
        if admin:
            return jsonify(admin), 200
        else:
            return jsonify({'error': 'Admin no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Crear un nuevo admin
@admins_bp.route('/insertar', methods=['POST'])
def create_admin():
    data = request.get_json()
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO admins (nombre, ap_P, ap_M, direccion, telefono, email, sexo, no_empleado, grado_estudios)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data['nombre'],
                data['ap_P'],
                data['ap_M'],
                data['direccion'],
                data['telefono'],
                data['email'],
                data['sexo'],
                data['no_empleado'],
                data['grado_estudios']
            ))
            conn.commit()
            admin_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': admin_id, **data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Actualizar un admin
@admins_bp.route('/editar/<int:id>', methods=['PUT'])
def update_admin(id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                UPDATE admins 
                SET nombre=%s, ap_P=%s, ap_M=%s, direccion=%s, telefono=%s, email=%s, sexo=%s, no_empleado=%s, grado_estudios=%s
                WHERE id_admins=%s
            """
            cursor.execute(sql, (
                data['nombre'],
                data['ap_P'],
                data['ap_M'],
                data['direccion'],
                data['telefono'],
                data['email'],
                data['sexo'],
                data['no_empleado'],
                data['grado_estudios'],
                id
            ))
            conn.commit()
        conn.close()
        return jsonify({'id': id, **data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Eliminar un admin
@admins_bp.route('/eliminar/<int:id>', methods=['DELETE'])
def delete_admin(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM admins WHERE id_admins = %s", (id,))
            conn.commit()
        conn.close()
        return jsonify({'result': 'Admin eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
