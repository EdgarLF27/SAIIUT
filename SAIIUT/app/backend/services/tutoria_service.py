from config import with_db_connection

class TutoriaError(Exception):
    """Excepción personalizada para errores de negocio en tutorías."""
    pass

@with_db_connection
def asignar_tutor_a_grupo(cursor, id_profesor, id_grupo):
    # Verificar si el grupo ya tiene un tutor
    cursor.execute("SELECT id_profesor_tutor FROM tutorias WHERE id_grupo = %s", (id_grupo,))
    if cursor.fetchone():
        raise TutoriaError(f"El grupo con ID {id_grupo} ya tiene un tutor asignado.")
    
    # Asignar el nuevo tutor
    sql = """
    INSERT INTO tutorias (id_profesor_tutor, id_grupo)
    VALUES (%s, %s)
    RETURNING id_tutoria;
    """
    cursor.execute(sql, (id_profesor, id_grupo))
    tutoria_id = cursor.fetchone()['id_tutoria']
    return {'id_tutoria': tutoria_id, 'id_profesor_tutor': id_profesor, 'id_grupo': id_grupo}

@with_db_connection
def obtener_tutor_de_grupo(cursor, id_grupo):
    cursor.execute("""
        SELECT p.id_profesor, p.nombre, p."ap_P", p."ap_M", p.no_empleado
        FROM profesores p
        JOIN tutorias t ON p.id_profesor = t.id_profesor_tutor
        WHERE t.id_grupo = %s
    """, (id_grupo,))
    row = cursor.fetchone()
    return dict(row) if row else None

@with_db_connection
def obtener_grupos_de_tutor(cursor, id_profesor):
    cursor.execute("""
        SELECT g.id_grupo, g.nombre_grupo, c.nombre_carrera
        FROM grupos g
        JOIN tutorias t ON g.id_grupo = t.id_grupo
        JOIN carreras c ON g.id_carrera = c.id_carrera
        WHERE t.id_profesor_tutor = %s
    """, (id_profesor,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@with_db_connection
def quitar_asignacion_tutor(cursor, id_grupo):
    # Se quita por id_grupo ya que un grupo solo puede tener un tutor
    cursor.execute("DELETE FROM tutorias WHERE id_grupo = %s", (id_grupo,))
    return cursor.rowcount > 0
