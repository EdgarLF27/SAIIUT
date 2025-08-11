from config import with_db_connection
import services.usuario_service as usuario_service

#Decorador para manejar la conexión a la base de datos
@with_db_connection
#Función para obtener todos los alumnos de la base de datos
def get_all_alumnos(cursor, filtros):
    sql = "SELECT * FROM alumnos"
    params = []
    conditions = []

    if filtros.get("nombre"):
        conditions.append("(nombre LIKE %s OR ap_P LIKE %s OR ap_M LIKE %s)")
        search_term = f"%{filtros['nombre']}%"
        params.extend([search_term, search_term, search_term])
    if filtros.get("apellido"):
        conditions.append("(ap_P LIKE %s OR ap_M LIKE %s)")
        search_term = f"%{filtros['apellido']}%"
        params.extend([search_term, search_term])
    if filtros.get("matricula"):
        conditions.append("matricula LIKE %s")
        params.append(f"%{filtros['matricula']}%")
    if filtros.get("carrera"):
        conditions.append("carrera = %s")
        params.append(filtros["carrera"])

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    cursor.execute(sql, tuple(params))
    return cursor.fetchall()


@with_db_connection
# Función para buscar un alumno por ID
def get_alumno_by_id(cursor, id):
    cursor.execute("SELECT * FROM alumnos WHERE id_alumno = %s", (id,))
    return cursor.fetchone()


@with_db_connection
#Función para crear un alumno
def create_alumno(cursor, data):
    username = data['matricula']
    user_id, temp_password = usuario_service.create_user_and_get_id(username)

    sql = """
    INSERT INTO alumnos (nombre, ap_P, ap_M, matricula, telefono, email, carrera, grado, grupo, sexo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data['nombre'], data['ap_P'], data['ap_M'], data['matricula'], 
        data['telefono'], data['email'], data['carrera'], 
        data['grado'], data['grupo'], data['sexo']
    ))
    alumno_id = cursor.lastrowid
    
    # Devolvemos los datos del alumno y la contraseña para el email
    return {'id': alumno_id, **data}, temp_password


@with_db_connection
#Función para actualizar un alumno
def update_alumno(cursor, id, data):
    # Nota: Por ahora, la actualización no modifica la matrícula/usuario.
    sql = """
    UPDATE alumnos
    SET nombre=%s, ap_P=%s, ap_M=%s, telefono=%s, email=%s, carrera=%s, grado=%s, grupo=%s, sexo=%s
    WHERE id_alumno=%s
    """
    cursor.execute(sql, (
        data['nombre'], data['ap_P'], data['ap_M'], 
        data['telefono'], data['email'], data['carrera'], 
        data['grado'], data['grupo'], data['sexo'], id
    ))
    return cursor.rowcount > 0


@with_db_connection
def delete_alumno(cursor, id):
    # Futura mejora: decidir si al eliminar un alumno se elimina también su 'usuario'.
    # Por ahora, solo se elimina el perfil del alumno.
    cursor.execute("DELETE FROM alumnos WHERE id_alumno = %s", (id,))
    return cursor.rowcount > 0