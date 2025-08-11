from config import with_db_connection
import services.usuario_service as usuario_service


@with_db_connection
def get_all_admins(cursor, filtros):
    sql = "SELECT id_admins, nombre, ap_P, ap_M, direccion, telefono, email, sexo, no_empleado, grado_estudios FROM admins"
    params = []

    if filtros.get("nombre"):
        sql += " WHERE nombre LIKE %s OR ap_P LIKE %s OR ap_M LIKE %s"
        search_term = f"%{filtros['nombre']}%"
        params.extend([search_term, search_term, search_term])

    cursor.execute(sql, tuple(params))
    return cursor.fetchall()


@with_db_connection
def get_admin_by_id(cursor, id):
    # Excluimos el campo 'password' por seguridad
    cursor.execute(
        "SELECT id_admins, nombre, ap_P, ap_M, direccion, telefono, email, sexo, no_empleado, grado_estudios FROM admins WHERE id_admins = %s",
        (id,),
    )
    return cursor.fetchone()


@with_db_connection
def create_admin(cursor, data):
    # Paso 1: Crear el usuario y obtener su ID y contraseña temporal
    username = data["no_empleado"]
    user_id, temp_password = usuario_service.create_user_and_get_id(username)

    # Paso 2: Insertar el admin, incluyendo el id_usuario para vincularlo
    sql = """
    INSERT INTO admins (nombre, ap_P, ap_M, direccion, telefono, email, sexo, no_empleado, grado_estudios, id_usuario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(
        sql,
        (
            data["nombre"],
            data["ap_P"],
            data["ap_M"],
            data["direccion"],
            data["telefono"],
            data["email"],
            data["sexo"],
            data["no_empleado"],
            data["grado_estudios"],
            user_id,  # Vinculamos con el usuario creado
        ),
    )
    admin_id = cursor.lastrowid
    
    # Devolvemos los datos del admin y la contraseña para el log/email
    return {"id": admin_id, **data}, temp_password


@with_db_connection
def update_admin(cursor, id, data):
    sql = """
    UPDATE admins
    SET nombre=%s, ap_P=%s, ap_M=%s, direccion=%s, telefono=%s, email=%s, sexo=%s, no_empleado=%s, grado_estudios=%s
    WHERE id_admins=%s
    """
    cursor.execute(
        sql,
        (
            data["nombre"],
            data["ap_P"],
            data["ap_M"],
            data["direccion"],
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
    cursor.execute("DELETE FROM admins WHERE id_admins = %s", (id,))
    return cursor.rowcount > 0
