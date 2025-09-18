from config import with_db_connection

@with_db_connection
def get_all_grupos(cursor):
    cursor.execute("""
        SELECT 
            g.id_grupo, 
            g.nombre_grupo, 
            g.id_carrera, 
            c.nombre_carrera
        FROM grupos g
        JOIN carreras c ON g.id_carrera = c.id_carrera
        ORDER BY g.nombre_grupo
    """)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@with_db_connection
def get_grupo_by_id(cursor, id):
    cursor.execute("""
        SELECT 
            g.id_grupo, 
            g.nombre_grupo, 
            g.id_carrera, 
            c.nombre_carrera
        FROM grupos g
        JOIN carreras c ON g.id_carrera = c.id_carrera
        WHERE g.id_grupo = %s
    """, (id,))
    row = cursor.fetchone()
    return dict(row) if row else None

@with_db_connection
def create_grupo(cursor, data):
    sql = """
    INSERT INTO grupos (nombre_grupo, id_carrera)
    VALUES (%s, %s)
    RETURNING id_grupo;
    """
    cursor.execute(sql, (data['nombre_grupo'], data['id_carrera']))
    grupo_id = cursor.fetchone()['id_grupo']
    return {'id_grupo': grupo_id, **data}

@with_db_connection
def update_grupo(cursor, id, data):
    sql = """
    UPDATE grupos
    SET nombre_grupo = %s, id_carrera = %s
    WHERE id_grupo = %s
    """
    cursor.execute(sql, (data['nombre_grupo'], data['id_carrera'], id))
    return cursor.rowcount > 0

@with_db_connection
def delete_grupo(cursor, id):
    cursor.execute('DELETE FROM grupos WHERE id_grupo = %s', (id,))
    return cursor.rowcount > 0
