from config import with_db_connection

@with_db_connection
def get_all_carreras(cursor):
    cursor.execute('SELECT id_carrera, nombre_carrera, abreviatura, total_cuatrimestres FROM carreras ORDER BY nombre_carrera')
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@with_db_connection
def get_carrera_by_id(cursor, id):
    cursor.execute('SELECT id_carrera, nombre_carrera, abreviatura, total_cuatrimestres FROM carreras WHERE id_carrera = %s', (id,))
    row = cursor.fetchone()
    return dict(row) if row else None

@with_db_connection
def create_carrera(cursor, data):
    sql = """
    INSERT INTO carreras (nombre_carrera, abreviatura, total_cuatrimestres)
    VALUES (%s, %s, %s)
    RETURNING id_carrera;
    """
    cursor.execute(sql, (data['nombre_carrera'], data['abreviatura'], data['total_cuatrimestres']))
    carrera_id = cursor.fetchone()['id_carrera']
    return {'id_carrera': carrera_id, **data}

@with_db_connection
def update_carrera(cursor, id, data):
    sql = """
    UPDATE carreras
    SET nombre_carrera = %s, abreviatura = %s, total_cuatrimestres = %s
    WHERE id_carrera = %s
    """
    cursor.execute(sql, (data['nombre_carrera'], data['abreviatura'], data['total_cuatrimestres'], id))
    return cursor.rowcount > 0

@with_db_connection
def delete_carrera(cursor, id):
    cursor.execute('DELETE FROM carreras WHERE id_carrera = %s', (id,))
    return cursor.rowcount > 0
