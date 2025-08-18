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
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


@with_db_connection
# Función para buscar un alumno por ID
def get_alumno_by_id(cursor, id):
    cursor.execute("SELECT * FROM alumnos WHERE id_alumno = %s", (id,))
    row = cursor.fetchone()
    return dict(row) if row else None


@with_db_connection
# Función para crear un alumno
def create_alumno(cursor, data):
<<<<<<< HEAD
    # Paso 1: Crear el usuario y obtener su ID y contraseña temporal
    username = data['matricula']
    user_id, temp_password = usuario_service.create_user_and_get_id(username)

    # Paso 2: Insertar el alumno (SIN el id_usuario)
    sql_insert = """
    INSERT INTO alumnos (nombre, ap_P, ap_M, matricula, telefono, email, carrera, grado, grupo, sexo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_insert, (
        data['nombre'], data['ap_P'], data['ap_M'], data['matricula'], 
        data['telefono'], data['email'], data['carrera'], 
        data['grado'], data['grupo'], data['sexo']
    ))
    alumno_id = cursor.lastrowid

    # Paso 3: Vincular el usuario con el alumno recién creado
    if user_id:
        sql_update = "UPDATE alumnos SET id_usuario = %s WHERE id_alumno = %s"
        cursor.execute(sql_update, (user_id, alumno_id))
    
=======
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

>>>>>>> ffa877abab98c35dea0184ab307c3af44900f407
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
    # Paso 1: Obtener el id_usuario antes de borrar el alumno
    cursor.execute("SELECT id_usuario FROM alumnos WHERE id_alumno = %s", (id,))
    result = cursor.fetchone()
    if not result:
        return 0  # El alumno no existía

    id_usuario_a_eliminar = result["id_usuario"]

    # Paso 2: Eliminar el registro del alumno
    cursor.execute("DELETE FROM alumnos WHERE id_alumno = %s", (id,))
    rows_deleted = cursor.rowcount

    # Paso 3: Eliminar el registro de usuario correspondiente
    if rows_deleted > 0 and id_usuario_a_eliminar:
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario_a_eliminar,))

    return rows_deleted > 0
