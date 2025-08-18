from config import with_db_connection

@with_db_connection
def asignar_materia_a_profesor(cursor, id_profesor, id_materia):
    sql = """
    INSERT INTO profesor_materias (id_profesor, id_materia)
    VALUES (%s, %s)
    ON CONFLICT (id_profesor, id_materia) DO NOTHING;
    """
    cursor.execute(sql, (id_profesor, id_materia))
    # rowcount nos dirá si se insertó una nueva fila (1) o si ya existía (0)
    return cursor.rowcount > 0

@with_db_connection
def obtener_materias_de_profesor(cursor, id_profesor):
    cursor.execute("""
        SELECT m.id_materia, m.nombre_materia, c.nombre_carrera
        FROM materias m
        JOIN profesor_materias pm ON m.id_materia = pm.id_materia
        JOIN carreras c ON m.id_carrera = c.id_carrera
        WHERE pm.id_profesor = %s
        ORDER BY m.nombre_materia
    """, (id_profesor,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@with_db_connection
def obtener_profesores_de_materia(cursor, id_materia):
    cursor.execute("""
        SELECT p.id_profesor, p.nombre, p."ap_P", p."ap_M", p.no_empleado
        FROM profesores p
        JOIN profesor_materias pm ON p.id_profesor = pm.id_profesor
        WHERE pm.id_materia = %s
        ORDER BY p."ap_P", p.nombre
    """, (id_materia,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@with_db_connection
def quitar_materia_a_profesor(cursor, id_profesor, id_materia):
    sql = "DELETE FROM profesor_materias WHERE id_profesor = %s AND id_materia = %s"
    cursor.execute(sql, (id_profesor, id_materia))
    return cursor.rowcount > 0
