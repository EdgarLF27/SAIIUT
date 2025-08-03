from config import with_db_connection


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
    sql = """
    INSERT INTO profesores (nombre, ap_P, ap_M, telefono, email, no_empleado, grado_estudio, sexo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
        ),
    )
    profesor_id = cursor.lastrowid
    return {"id": profesor_id, **data}


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
