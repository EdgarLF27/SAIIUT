from config import with_db_connection

@with_db_connection
def get_alumnos_con_calificaciones(cursor, id_profesor, id_grupo, id_materia):
    """
    Obtiene la lista de alumnos inscritos en una materia y grupo específicos
    impartidos por un profesor, junto con sus calificaciones.
    """
    sql = """
        SELECT
            a.id_alumno,
            a.nombre,
            a."ap_P",
            a."ap_M",
            a.matricula,
            cal.id_calificacion,
            cal.parcial_1,
            cal.parcial_2,
            cal.parcial_3,
            cal.calificacion_final
        FROM alumnos a
        JOIN inscripciones i ON a.id_alumno = i.id_alumno
        LEFT JOIN calificaciones cal ON i.id_inscripcion = cal.id_inscripcion
        WHERE i.id_grupo = %s
          AND i.id_materia = %s
          AND i.id_profesor = %s
        ORDER BY a."ap_P", a."ap_M", a.nombre;
    """
    cursor.execute(sql, (id_grupo, id_materia, id_profesor))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@with_db_connection
def actualizar_calificacion(cursor, id_calificacion, parcial, calificacion):
    """
    Actualiza la calificación de un parcial específico para un registro de calificación.
    Valida que el nombre del parcial sea uno de los permitidos para evitar inyección SQL.
    """
    parciales_validos = ["parcial_1", "parcial_2", "parcial_3", "calificacion_final"]
    if parcial not in parciales_validos:
        raise ValueError("Nombre de parcial no válido.")

    # El nombre de la columna se inserta de forma segura, no por el usuario.
    sql = f"""
        UPDATE calificaciones
        SET {parcial} = %s
        WHERE id_calificacion = %s;
    """
    cursor.execute(sql, (calificacion, id_calificacion))
    return cursor.rowcount > 0
