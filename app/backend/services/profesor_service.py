from config import with_db_connection
import services.usuario_service as usuario_service


@with_db_connection
def get_all_profesores(cursor, filtros):
    sql = "SELECT id_profesor, nombre, ap_P, ap_M, telefono, email, no_empleado, grado_estudio, sexo FROM profesores"
    params = []

    if filtros.get("nombre"):
        sql += " WHERE nombre LIKE %s OR ap_P LIKE %s OR ap_M LIKE %s"
        search_term = f"%{filtros['nombre']}%"
        params.extend([search_term, search_term, search_term])

    cursor.execute(sql, tuple(params))
    return cursor.fetchall()


@with_db_connection
def get_profesor_by_id(cursor, id):
    cursor.execute(
        "SELECT id_profesor, nombre, ap_P, ap_M, telefono, email, no_empleado, grado_estudio, sexo FROM profesores WHERE id_profesor = %s",
        (id,),
    )
    return cursor.fetchone()


@with_db_connection
def create_profesor(cursor, data):
    # Paso 1: Crear el usuario y obtener su ID y contraseña temporal
    username = data["no_empleado"]
    user_id, temp_password = usuario_service.create_user_and_get_id(username)

    # Paso 2: Insertar el profesor, incluyendo el id_usuario para vincularlo
    sql = """
    INSERT INTO profesores (nombre, ap_P, ap_M, telefono, email, no_empleado, grado_estudio, sexo, id_usuario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
    profesor_id = cursor.lastrowid
    
    # Devolvemos los datos del profesor y la contraseña para el log/email
    return {"id": profesor_id, **data}, temp_password


@with_db_connection
def update_profesor(cursor, id, data):
    sql = """
    UPDATE profesores
    SET nombre=%s, ap_P=%s, ap_M=%s, telefono=%s, email=%s, no_empleado=%s, grado_estudio=%s, sexo=%s
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
    cursor.execute("DELETE FROM profesores WHERE id_profesor = %s", (id,))
    return cursor.rowcount > 0
