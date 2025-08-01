from config import with_db_connection


@with_db_connection
def get_all_alumnos(cursor, filtros=None):
    sql = "SELECT * FROM alumnos"
    conditions = []
    params = []

    if filtros:
        if filtros.get('nombre'):
            # Busca el nombre en cualquiera de los campos de nombre o apellido
            conditions.append("(nombre LIKE %s OR ap_P LIKE %s OR ap_M LIKE %s)")
            search_nombre = f"%{filtros['nombre']}%"
            params.extend([search_nombre, search_nombre, search_nombre])
        
        if filtros.get('apellido'):
            conditions.append("(ap_P LIKE %s OR ap_M LIKE %s)")
            search_apellido = f"%{filtros['apellido']}%"
            params.extend([search_apellido, search_apellido])

        if filtros.get('carrera'):
            conditions.append("carrera = %s")
            params.append(filtros['carrera'])
        
        if filtros.get('matricula'):
            conditions.append("matricula = %s")
            params.append(filtros['matricula'])

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
