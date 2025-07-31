from config import with_db_connection

@with_db_connection
def get_all_admins(cursor):
    # Excluimos el campo 'password' por seguridad
    cursor.execute("SELECT id_admins, nombre, ap_P, ap_M, direccion, telefono, email, sexo, no_empleado, grado_estudios FROM admins")
    return cursor.fetchall()

@with_db_connection
def get_admin_by_id(cursor, id):
    # Excluimos el campo 'password' por seguridad
    cursor.execute("SELECT id_admins, nombre, ap_P, ap_M, direccion, telefono, email, sexo, no_empleado, grado_estudios FROM admins WHERE id_admins = %s", (id,))
    return cursor.fetchone()

@with_db_connection
def create_admin(cursor, data):
    sql = """
    INSERT INTO admins (nombre, ap_P, ap_M, direccion, telefono, email, sexo, no_empleado, grado_estudios)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data['nombre'], data['ap_P'], data['ap_M'], data['direccion'], 
        data['telefono'], data['email'], data['sexo'], 
        data['no_empleado'], data['grado_estudios']
    ))
    admin_id = cursor.lastrowid
    # No devolvemos el password
    return {'id': admin_id, **data}

@with_db_connection
def update_admin(cursor, id, data):
    sql = """
    UPDATE admins
    SET nombre=%s, ap_P=%s, ap_M=%s, direccion=%s, telefono=%s, email=%s, sexo=%s, no_empleado=%s, grado_estudios=%s
    WHERE id_admins=%s
    """
    cursor.execute(sql, (
        data['nombre'], data['ap_P'], data['ap_M'], data['direccion'], 
        data['telefono'], data['email'], data['sexo'], 
        data['no_empleado'], data['grado_estudios'], id
    ))
    # rowcount nos dice cuántas filas fueron afectadas. Si es 0, no se encontró el admin.
    return cursor.rowcount > 0

@with_db_connection
def delete_admin(cursor, id):
    cursor.execute("DELETE FROM admins WHERE id_admins = %s", (id,))
    return cursor.rowcount > 0

