from config import with_db_connection


@with_db_connection
def get_all_alumnos(cursor, filtros):
    sql = "SELECT * FROM alumnos"
    params = []
    conditions = []

    # Filtro por nombre o apellido (búsqueda parcial)
    if filtros.get("nombre"):
        conditions.append("(nombre LIKE %s OR ap_P LIKE %s OR ap_M LIKE %s)")
        search_term = f"%{filtros['nombre']}%"
        params.extend([search_term, search_term, search_term])

    if filtros.get("apellido"):
        conditions.append("(ap_P LIKE %s OR ap_M LIKE %s)")
        search_term = f"%{filtros['apellido']}%"
        params.extend([search_term, search_term])

    # Filtro por matrícula (búsqueda parcial, por si escriben solo el inicio)
    if filtros.get("matricula"):
        conditions.append("matricula LIKE %s")
        params.append(f"%{filtros['matricula']}%")

    # Filtro por carrera (búsqueda exacta)
    if filtros.get("carrera"):
        conditions.append("carrera = %s")
        params.append(filtros["carrera"])

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    cursor.execute(sql, tuple(params))
    return cursor.fetchall()


@with_db_connection
def get_alumno_by_id(cursor, id):
    cursor.execute("SELECT * FROM alumnos WHERE id_alumno = %s", (id,))
    return cursor.fetchone()


@with_db_connection
def create_alumno(cursor, data):
    sql = """
    INSERT INTO alumnos (nombre, ap_P, ap_M, matricula, telefono, email, carrera, grado, grupo, sexo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(
        sql,
        (
            data["nombre"],
            data["ap_P"],
            data["ap_M"],
            data["matricula"],
            data["telefono"],
            data["email"],
            data["carrera"],
            data["grado"],
            data["grupo"],
            data["sexo"],
        ),
    )
    alumno_id = cursor.lastrowid
    return {"id": alumno_id, **data}


@with_db_connection
def update_alumno(cursor, id, data):
    sql = """
    UPDATE alumnos
    SET nombre=%s, ap_P=%s, ap_M=%s, matricula=%s, telefono=%s, email=%s, carrera=%s, grado=%s, grupo=%s, sexo=%s
    WHERE id_alumno=%s
    """
    cursor.execute(
        sql,
        (
            data["nombre"],
            data["ap_P"],
            data["ap_M"],
            data["matricula"],
            data["telefono"],
            data["email"],
            data["carrera"],
            data["grado"],
            data["grupo"],
            data["sexo"],
            id,
        ),
    )
    return cursor.rowcount > 0


@with_db_connection
def delete_alumno(cursor, id):
    cursor.execute("DELETE FROM alumnos WHERE id_alumno = %s", (id,))
    return cursor.rowcount > 0
