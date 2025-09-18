import services.usuario_service as usuario_service
from config import with_db_connection


@with_db_connection
def get_all_profesores(cursor, filtros):
    sql = 'SELECT id_profesor, nombre, "ap_P", "ap_M", telefono, email, no_empleado, grado_estudio, sexo FROM profesores'
    params = []

    if filtros.get("nombre"):
        sql += ' WHERE nombre LIKE %s OR "ap_P" LIKE %s OR "ap_M" LIKE %s'
        search_term = f"%{filtros['nombre']}%"
        params.extend([search_term, search_term, search_term])

    cursor.execute(sql, tuple(params))
    # Convertir cada fila (que es un objeto tipo tupla/diccionario) a un diccionario estándar
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


@with_db_connection
def get_profesor_by_id(cursor, id):
    cursor.execute(
        'SELECT id_profesor, nombre, "ap_P", "ap_M", telefono, email, no_empleado, grado_estudio, sexo FROM profesores WHERE id_profesor = %s',
        (id,),
    )
    row = cursor.fetchone()
    # Convertir la fila a un diccionario estándar si existe
    return dict(row) if row else None


@with_db_connection
def create_profesor(cursor, data):
    # Paso 1: Crear el usuario y obtener su ID y contraseña temporal
    username = data["no_empleado"]
    # Se debe pasar el cursor a la función interna para mantener la transacción
    user_id, temp_password = usuario_service._create_user_and_get_id_internal(
        cursor, username
    )

    # Si el usuario ya existía, la función devuelve (id, None)
    if temp_password is None:
        return None, None

    # Paso 2: Insertar el profesor, incluyendo el id_usuario para vincularlo
    sql = """
    INSERT INTO profesores (nombre, "ap_P", "ap_M", telefono, email, no_empleado, grado_estudio, sexo, id_usuario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id_profesor;
    """
    cursor.execute(
        sql,
        (
            data["nombre"],
            data["ap_P"],
            data["ap_M"],
            data["telefono"],
            data["email"],
            data["no_empleado"],
            data["grado_estudio"],
            data["sexo"],
            user_id,  # Vinculamos con el usuario creado
        ),
    )
    # Obtenemos el ID devuelto por la consulta RETURNING
    profesor_id = cursor.fetchone()["id_profesor"]

    # Devolvemos los datos del profesor y la contraseña para el log/email
    return {"id": profesor_id, **data}, temp_password


@with_db_connection
def update_profesor(cursor, id, data):
    sql = """
    UPDATE profesores
    SET nombre=%s, "ap_P"=%s, "ap_M"=%s, telefono=%s, email=%s, no_empleado=%s, grado_estudio=%s, sexo=%s
    WHERE id_profesor=%s
    """
    cursor.execute(
        sql,
        (
            data["nombre"],
            data["ap_P"],
            data["ap_M"],
            data["telefono"],
            data["email"],
            data["no_empleado"],
            data["grado_estudio"],
            data["sexo"],
            id,
        ),
    )
    return cursor.rowcount > 0


@with_db_connection
def delete_profesor(cursor, id):
    # Paso 1: Obtener el id_usuario antes de borrar nada
    cursor.execute("SELECT id_usuario FROM profesores WHERE id_profesor = %s", (id,))
    result = cursor.fetchone()
    if not result:
        return 0  # El profesor no existía

    id_usuario_a_eliminar = result["id_usuario"]

    # Paso 2: Eliminar dependencias en cadena para evitar errores de FK
    # 2a: Eliminar calificaciones ligadas a las inscripciones del profesor
    cursor.execute("""
        DELETE FROM calificaciones 
        WHERE id_inscripcion IN (SELECT id_inscripcion FROM inscripciones WHERE id_profesor = %s)
    """, (id,))
    
    # 2b: Eliminar inscripciones donde el profesor imparte clase
    cursor.execute("DELETE FROM inscripciones WHERE id_profesor = %s", (id,))
    
    # 2c: Eliminar tutorías asignadas al profesor
    cursor.execute("DELETE FROM tutorias WHERE id_profesor_tutor = %s", (id,))
    
    # 2d: Eliminar asignaciones de materias del profesor
    cursor.execute("DELETE FROM profesor_materias WHERE id_profesor = %s", (id,))

    # Paso 3: Eliminar el registro del profesor
    cursor.execute("DELETE FROM profesores WHERE id_profesor = %s", (id,))
    rows_deleted = cursor.rowcount

    # Paso 4: Eliminar el registro de usuario correspondiente
    if rows_deleted > 0 and id_usuario_a_eliminar:
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario_a_eliminar,))

    return rows_deleted > 0
