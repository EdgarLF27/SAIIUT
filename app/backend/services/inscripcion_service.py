from config import with_db_connection

class InscripcionError(Exception):
    """Excepción para errores de negocio en inscripciones."""
    pass

@with_db_connection
def inscribir_alumno_en_grupo(cursor, id_alumno, id_grupo):
    # 1. Validaciones previas
    cursor.execute("SELECT id_carrera, id_periodo FROM grupos WHERE id_grupo = %s", (id_grupo,))
    grupo = cursor.fetchone()
    if not grupo:
        raise InscripcionError("El grupo especificado no existe.")

    cursor.execute("SELECT 1 FROM alumnos WHERE id_alumno = %s", (id_alumno,))
    if not cursor.fetchone():
        raise InscripcionError("El alumno especificado no existe.")

    # Evitar doble inscripción del alumno en el mismo grupo/periodo
    cursor.execute("SELECT 1 FROM inscripciones WHERE id_alumno = %s AND id_grupo = %s", (id_alumno, id_grupo))
    if cursor.fetchone():
        raise InscripcionError("El alumno ya está inscrito en este grupo.")

    # 2. Obtener materias de la carrera del grupo
    id_carrera = grupo['id_carrera']
    cursor.execute("SELECT id_materia FROM materias WHERE id_carrera = %s", (id_carrera,))
    materias = cursor.fetchall()
    if not materias:
        raise InscripcionError("No se encontraron materias para la carrera de este grupo.")

    inscripciones_creadas = []

    # 3. Bucle principal: crear inscripción y calificación por cada materia
    for materia in materias:
        id_materia = materia['id_materia']

        # 3a. Encontrar un profesor para la materia (simplificación: el primero disponible)
        cursor.execute("SELECT id_profesor FROM profesor_materias WHERE id_materia = %s LIMIT 1", (id_materia,))
        profesor_asignado = cursor.fetchone()
        if not profesor_asignado:
            raise InscripcionError(f"No hay un profesor asignado para la materia ID {id_materia}. No se puede completar la inscripción.")
        
        id_profesor = profesor_asignado['id_profesor']

        # 3b. Crear el registro en la tabla 'inscripciones'
        sql_inscripcion = """
        INSERT INTO inscripciones (id_alumno, id_grupo, id_materia, id_profesor)
        VALUES (%s, %s, %s, %s)
        RETURNING id_inscripcion;
        """
        cursor.execute(sql_inscripcion, (id_alumno, id_grupo, id_materia, id_profesor))
        id_inscripcion = cursor.fetchone()['id_inscripcion']

        # 3c. Crear el registro de calificaciones vacío
        sql_calificacion = "INSERT INTO calificaciones (id_inscripcion) VALUES (%s)"
        cursor.execute(sql_calificacion, (id_inscripcion,))
        
        inscripciones_creadas.append(id_inscripcion)

    return {"message": f"Alumno inscrito exitosamente en {len(inscripciones_creadas)} materias.", "inscripciones_ids": inscripciones_creadas}

@with_db_connection
def obtener_inscripciones_de_alumno(cursor, id_alumno, id_periodo=None):
    sql = """
        SELECT 
            i.id_inscripcion,
            m.nombre_materia,
            g.nombre_grupo,
            p.nombre AS nombre_profesor,
            p.ap_P AS ap_P_profesor,
            c.parcial_1, c.parcial_2, c.parcial_3, c.calificacion_final
        FROM inscripciones i
        JOIN materias m ON i.id_materia = m.id_materia
        JOIN grupos g ON i.id_grupo = g.id_grupo
        JOIN profesores p ON i.id_profesor = p.id_profesor
        LEFT JOIN calificaciones c ON i.id_inscripcion = c.id_inscripcion
        WHERE i.id_alumno = %s
    """
    params = [id_alumno]
    if id_periodo:
        sql += " AND g.id_periodo = %s"
        params.append(id_periodo)
    
    cursor.execute(sql, tuple(params))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
