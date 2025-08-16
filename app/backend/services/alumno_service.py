import services.usuario_service as usuario_service
from config import with_db_connection


# Decorador para manejar la conexión a la base de datos
@with_db_connection
# Función para obtener todos los alumnos de la base de datos
def get_all_alumnos(cursor, filtros):
    sql = "SELECT * FROM alumnos"
    params = []
    conditions = []

    if filtros.get("nombre"):
        conditions.append('(nombre LIKE %s OR "ap_P" LIKE %s OR "ap_M" LIKE %s)')
        search_term = f"%{filtros['nombre']}%"
        params.extend([search_term, search_term, search_term])
    if filtros.get("apellido"):
        conditions.append('("ap_P" LIKE %s OR "ap_M" LIKE %s)')
        search_term = f"%{filtros['apellido']}%"
        params.extend([search_term, search_term])
    if filtros.get("matricula"):
        conditions.append("matricula LIKE %s")
        params.append(f"%{filtros['matricula']}%")
    if filtros.get("carrera"):
        conditions.append("carrera = %s")
        params.append(filtros["carrera"])

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    cursor.execute(sql, tuple(params))
    return cursor.fetchall()


@with_db_connection
# Función para buscar un alumno por ID
def get_alumno_by_id(cursor, id):
    cursor.execute("SELECT * FROM alumnos WHERE id_alumno = %s", (id,))
    return cursor.fetchone()


@with_db_connection
# Función para crear un alumno
def create_alumno(cursor, data):
    # Paso 1: Crear el usuario DENTRO de la misma transacción
    username = data["matricula"]
    # Llamamos a la función interna, pasándole nuestro cursor actual
    user_id, temp_password = usuario_service._create_user_and_get_id_internal(
        cursor, username
    )

    # Si el usuario ya existía, create_user_and_get_id devuelve (id, None)
    if temp_password is None:
        # Devolvemos None para indicar que el alumno (por su matrícula) ya existe.
        return None, None

    # Paso 2: Insertar el alumno con la lista de columnas y valores corregida
    sql_insert = """
    INSERT INTO alumnos (id_usuario, nombre, "ap_P", "ap_M", matricula, telefono, email, sexo, id_carrera)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id_alumno;
    """
    cursor.execute(
        sql_insert,
        (
            user_id,
            data["nombre"],
            data["ap_P"],
            data["ap_M"],
            data["matricula"],
            data["telefono"],
            data["email"],
            data["sexo"],
            data["id_carrera"],
        ),
    )
    # Obtenemos el ID devuelto por la consulta RETURNING
    alumno_id = cursor.fetchone()["id_alumno"]

    # Devolvemos los datos del alumno y la contraseña para el email
    return {"id": alumno_id, **data}, temp_password


@with_db_connection
# Función para actualizar un alumno
def update_alumno(cursor, id, data):
    # Nota: Por ahora, la actualización no modifica la matrícula/usuario.
    sql = """
    UPDATE alumnos
    SET nombre=%s, "ap_P"=%s, "ap_M"=%s, matricula=%s, telefono=%s, email=%s, sexo=%s, id_carrera=%s
    WHERE id_alumno=%s
    """
    cursor.execute(
        sql,
        (
            data["nombre"],
            data["ap_P"],
            data["ap_M"],
            data["matricula"],
            data["telefono"],
            data["email"],
            data["sexo"],
            data["id_carrera"],
            id,
        ),
    )
    return cursor.rowcount > 0


@with_db_connection
def delete_alumno(cursor, id):
    # Futura mejora: decidir si al eliminar un alumno se elimina también su 'usuario'.
    # Por ahora, solo se elimina el perfil del alumno.
    cursor.execute("DELETE FROM alumnos WHERE id_alumno = %s", (id,))
    return cursor.rowcount > 0
