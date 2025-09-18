from config import with_db_connection

@with_db_connection
def get_all_cuatrimestres(cursor):
    """Obtiene todos los cuatrimestres ordenados por su número de orden."""
    cursor.execute("SELECT id_cuatrimestre, nombre, orden FROM cuatrimestres ORDER BY orden")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@with_db_connection
def get_cuatrimestre_by_id(cursor, id):
    """Obtiene un cuatrimestre específico por su ID."""
    cursor.execute("SELECT id_cuatrimestre, nombre, orden FROM cuatrimestres WHERE id_cuatrimestre = %s", (id,))
    row = cursor.fetchone()
    return dict(row) if row else None

@with_db_connection
def create_cuatrimestre(cursor, data):
    """Crea un nuevo cuatrimestre."""
    sql = """
    INSERT INTO cuatrimestres (nombre, orden)
    VALUES (%s, %s)
    RETURNING id_cuatrimestre;
    """
    cursor.execute(sql, (data['nombre'], data['orden']))
    cuatrimestre_id = cursor.fetchone()['id_cuatrimestre']
    return {'id_cuatrimestre': cuatrimestre_id, **data}

@with_db_connection
def update_cuatrimestre(cursor, id, data):
    """Actualiza un cuatrimestre existente."""
    sql = """
    UPDATE cuatrimestres
    SET nombre = %s, orden = %s
    WHERE id_cuatrimestre = %s
    """
    cursor.execute(sql, (data['nombre'], data['orden'], id))
    return cursor.rowcount > 0

@with_db_connection
def delete_cuatrimestre(cursor, id):
    """Elimina un cuatrimestre."""
    cursor.execute('DELETE FROM cuatrimestres WHERE id_cuatrimestre = %s', (id,))
    return cursor.rowcount > 0
