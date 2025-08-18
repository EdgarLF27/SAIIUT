import services.usuario_service as usuario_service
from config import with_db_connection


@with_db_connection
def get_all_admins(cursor, filtros):
    sql = 'SELECT id_admin, nombre, "ap_P", "ap_M", telefono, email, sexo, no_empleado, grado_estudios FROM admins'
    params = []

    if filtros.get("nombre"):
        sql += ' WHERE nombre LIKE %s OR "ap_P" LIKE %s OR "ap_M" LIKE %s'
        search_term = f"%{filtros['nombre']}%"
        params.extend([search_term, search_term, search_term])

    cursor.execute(sql, tuple(params))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


@with_db_connection
def get_admin_by_id(cursor, id):
    # Excluimos el campo 'password' por seguridad
    cursor.execute(
        'SELECT id_admin, nombre, "ap_P", "ap_M", telefono, email, sexo, no_empleado, grado_estudios FROM admins WHERE id_admin = %s',
        (id,),
    )
    row = cursor.fetchone()
    return dict(row) if row else None


@with_db_connection
def create_admin(cursor, data):
    # Paso 1: Crear el usuario y obtener su ID y contraseña temporal
    username = data["no_empleado"]
    # Se debe pasar el cursor a la función interna para mantener la transacción
    user_id, temp_password = usuario_service._create_user_and_get_id_internal(
        cursor, username
    )

    # Si el usuario ya existía, la función devuelve (id, None)
    if temp_password is None:
        return None, None

    # Paso 2: Insertar el admin, incluyendo el id_usuario para vincularlo
    sql = """
    INSERT INTO admins (nombre, "ap_P", "ap_M", telefono, email, sexo, no_empleado, grado_estudios, id_usuario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id_admin;
    """
    cursor.execute(
        sql,
        (
            data["nombre"],
            data["ap_P"],
            data["ap_M"],
            data["telefono"],
            data["email"],
            data["sexo"],
            data["no_empleado"],
            data["grado_estudios"],
            user_id,  # Vinculamos con el usuario creado
        ),
    )
    # Obtenemos el ID devuelto por la consulta RETURNING
    admin_id = cursor.fetchone()["id_admin"]

    # Devolvemos los datos del admin y la contraseña para el log/email
    return {"id": admin_id, **data}, temp_password


@with_db_connection
def update_admin(cursor, id, data):
    sql = """
    UPDATE admins
    SET nombre=%s, "ap_P"=%s, "ap_M"=%s, telefono=%s, email=%s, sexo=%s, no_empleado=%s, grado_estudios=%s
    WHERE id_admin=%s
    """
    cursor.execute(
        sql,
        (
            data["nombre"],
            data["ap_P"],
            data["ap_M"],
            data["telefono"],
            data["email"],
            data["sexo"],
            data["no_empleado"],
            data["grado_estudios"],
            id,
        ),
    )
    # rowcount nos dice cuántas filas fueron afectadas. Si es 0, no se encontró el admin.
    return cursor.rowcount > 0


@with_db_connection
def delete_admin(cursor, id):
    # Paso 1: Obtener el id_usuario antes de borrar el admin
    cursor.execute("SELECT id_usuario FROM admins WHERE id_admin = %s", (id,))
    result = cursor.fetchone()
    if not result:
        return 0  # El admin no existía

    id_usuario_a_eliminar = result["id_usuario"]

    # Paso 2: Eliminar el registro del admin
    cursor.execute("DELETE FROM admins WHERE id_admin = %s", (id,))
    rows_deleted = cursor.rowcount

    # Paso 3: Eliminar el registro de usuario correspondiente
    if rows_deleted > 0 and id_usuario_a_eliminar:
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario_a_eliminar,))

    return rows_deleted > 0
