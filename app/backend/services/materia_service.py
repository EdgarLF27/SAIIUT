from config import with_db_connection

@with_db_connection
def get_all_materias(cursor, id_carrera=None):
    sql = """
        SELECT 
            m.id_materia, 
            m.nombre_materia, 
            m.id_carrera, 
            c.nombre_carrera,
            cu.id_cuatrimestre,
            cu.nombre AS nombre_cuatrimestre,
            p.id_profesor,
            p.nombre AS nombre_profesor,
            p."ap_P" AS "ap_P_profesor",
            p."ap_M" AS "ap_M_profesor"
        FROM materias m
        JOIN carreras c ON m.id_carrera = c.id_carrera
        LEFT JOIN cuatrimestres cu ON m.id_cuatrimestre = cu.id_cuatrimestre
        LEFT JOIN profesor_materias pm ON m.id_materia = pm.id_materia
        LEFT JOIN profesores p ON pm.id_profesor = p.id_profesor
    """
    params = []
    if id_carrera:
        sql += " WHERE m.id_carrera = %s"
        params.append(id_carrera)
    
    sql += " ORDER BY m.nombre_materia"
    
    cursor.execute(sql, tuple(params))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@with_db_connection
def get_materia_by_id(cursor, id):
    cursor.execute("""
        SELECT 
            m.id_materia, 
            m.nombre_materia, 
            m.id_carrera, 
            m.id_cuatrimestre,
            c.nombre_carrera,
            p.id_profesor
        FROM materias m
        JOIN carreras c ON m.id_carrera = c.id_carrera
        LEFT JOIN profesor_materias pm ON m.id_materia = pm.id_materia
        LEFT JOIN profesores p ON pm.id_profesor = p.id_profesor
        WHERE m.id_materia = %s
    """, (id,))
    row = cursor.fetchone()
    return dict(row) if row else None

@with_db_connection
def create_materia(cursor, data):
    sql = """
    INSERT INTO materias (nombre_materia, id_carrera, id_cuatrimestre)
    VALUES (%s, %s, %s)
    RETURNING id_materia;
    """
    cursor.execute(sql, (data['nombre_materia'], data['id_carrera'], data.get('id_cuatrimestre')))
    materia_id = cursor.fetchone()['id_materia']
    
    # Si se proporcionó un profesor, crear la asignación en la tabla intermedia
    if data.get('id_profesor'):
        cursor.execute(
            "INSERT INTO profesor_materias (id_profesor, id_materia) VALUES (%s, %s)",
            (data['id_profesor'], materia_id)
        )
        
    return {'id_materia': materia_id, **data}

@with_db_connection
def update_materia(cursor, id, data):
    sql = """
    UPDATE materias
    SET nombre_materia = %s, id_carrera = %s, id_cuatrimestre = %s
    WHERE id_materia = %s
    """
    cursor.execute(sql, (data['nombre_materia'], data['id_carrera'], data.get('id_cuatrimestre'), id))
    
    # Actualizar la asignación del profesor:
    # 1. Borrar cualquier asignación existente para esta materia.
    cursor.execute("DELETE FROM profesor_materias WHERE id_materia = %s", (id,))
    
    # 2. Si se proporcionó un nuevo profesor, crear la nueva asignación.
    if data.get('id_profesor'):
        cursor.execute(
            "INSERT INTO profesor_materias (id_profesor, id_materia) VALUES (%s, %s)",
            (data['id_profesor'], id)
        )
        
    return cursor.rowcount > 0

@with_db_connection
def delete_materia(cursor, id):
    cursor.execute('DELETE FROM materias WHERE id_materia = %s', (id,))
    return cursor.rowcount > 0
