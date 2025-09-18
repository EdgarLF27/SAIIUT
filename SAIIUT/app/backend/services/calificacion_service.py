from config import with_db_connection

@with_db_connection
def get_all_calificaciones(cursor):
    # Esta consulta compleja nos da todo el contexto de una calificación
    cursor.execute("""
        SELECT 
            cal.id_calificacion,
            cal.id_inscripcion,
            cal.parcial_1,
            cal.parcial_2,
            cal.parcial_3,
            cal.calificacion_final,
            a.nombre AS nombre_alumno,
            a.ap_paterno,
            m.nombre_materia
        FROM calificaciones cal
        JOIN inscripciones i ON cal.id_inscripcion = i.id_inscripcion
        JOIN alumnos a ON i.id_alumno = a.id_alumno
        JOIN materias m ON i.id_materia = m.id_materia
    """)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@with_db_connection
def get_calificacion_by_id(cursor, id):
    cursor.execute("""
        SELECT 
            cal.id_calificacion, cal.id_inscripcion, cal.parcial_1, cal.parcial_2, cal.parcial_3, cal.calificacion_final,
            a.nombre AS nombre_alumno, a.ap_paterno, m.nombre_materia
        FROM calificaciones cal
        JOIN inscripciones i ON cal.id_inscripcion = i.id_inscripcion
        JOIN alumnos a ON i.id_alumno = a.id_alumno
        JOIN materias m ON i.id_materia = m.id_materia
        WHERE cal.id_calificacion = %s
    """, (id,))
    row = cursor.fetchone()
    return dict(row) if row else None

@with_db_connection
def create_calificacion(cursor, data):
    # Lógica simple para calcular el promedio si los tres parciales están presentes
    p1 = data.get('parcial_1')
    p2 = data.get('parcial_2')
    p3 = data.get('parcial_3')
    final = None
    if p1 is not None and p2 is not None and p3 is not None:
        final = round((p1 + p2 + p3) / 3, 2)

    sql = """
    INSERT INTO calificaciones (id_inscripcion, parcial_1, parcial_2, parcial_3, calificacion_final)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id_calificacion;
    """
    cursor.execute(sql, (data['id_inscripcion'], p1, p2, p3, final))
    calificacion_id = cursor.fetchone()['id_calificacion']
    return {'id_calificacion': calificacion_id, **data}

@with_db_connection
def update_calificacion(cursor, id, data):
    p1 = data.get('parcial_1')
    p2 = data.get('parcial_2')
    p3 = data.get('parcial_3')
    final = None
    if p1 is not None and p2 is not None and p3 is not None:
        final = round((p1 + p2 + p3) / 3, 2)

    sql = """
    UPDATE calificaciones
    SET parcial_1 = %s, parcial_2 = %s, parcial_3 = %s, calificacion_final = %s
    WHERE id_calificacion = %s
    """
    cursor.execute(sql, (p1, p2, p3, final, id))
    return cursor.rowcount > 0

@with_db_connection
def delete_calificacion(cursor, id):
    cursor.execute('DELETE FROM calificaciones WHERE id_calificacion = %s', (id,))
    return cursor.rowcount > 0
