from config import with_db_connection

@with_db_connection
def get_all_materias(cursor):
    # Unimos con carreras para obtener el nombre de la carrera, que es más útil para el frontend.
    cursor.execute("""
        SELECT m.id_materia, m.nombre_materia, m.id_carrera, c.nombre_carrera
        FROM materias m
        JOIN carreras c ON m.id_carrera = c.id_carrera
        ORDER BY m.nombre_materia
    """)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@with_db_connection
def get_materia_by_id(cursor, id):
    cursor.execute("""
        SELECT m.id_materia, m.nombre_materia, m.id_carrera, c.nombre_carrera
        FROM materias m
        JOIN carreras c ON m.id_carrera = c.id_carrera
        WHERE m.id_materia = %s
    """, (id,))
    row = cursor.fetchone()
    return dict(row) if row else None

@with_db_connection
def create_materia(cursor, data):
    sql = """
    INSERT INTO materias (nombre_materia, id_carrera)
    VALUES (%s, %s)
    RETURNING id_materia;
    """
    cursor.execute(sql, (data['nombre_materia'], data['id_carrera']))
    materia_id = cursor.fetchone()['id_materia']
    return {'id_materia': materia_id, **data}

@with_db_connection
def update_materia(cursor, id, data):
    sql = """
    UPDATE materias
    SET nombre_materia = %s, id_carrera = %s
    WHERE id_materia = %s
    """
    cursor.execute(sql, (data['nombre_materia'], data['id_carrera'], id))
    return cursor.rowcount > 0

@with_db_connection
def delete_materia(cursor, id):
    cursor.execute('DELETE FROM materias WHERE id_materia = %s', (id,))
    return cursor.rowcount > 0
