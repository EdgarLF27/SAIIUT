from config import with_db_connection

@with_db_connection
def get_alumnos_for_calificacion(cursor, id_grupo, id_materia):
    sql = """
    SELECT
        a.id_alumno,
        a.nombre,
        a.ap_P,
        a.ap_M,
        a.matricula,
        c.id_calificacion,
        c.parcial_1,
        c.parcial_2,
        c.parcial_3,
        c.calificacion_final
    FROM alumnos a
    JOIN inscripciones i ON a.id_alumno = i.id_alumno
    LEFT JOIN calificaciones c ON i.id_inscripcion = c.id_inscripcion
    WHERE i.id_grupo = %s AND i.id_materia = %s
    ORDER BY a.ap_P, a.ap_M, a.nombre;
    """
    cursor.execute(sql, (id_grupo, id_materia))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
