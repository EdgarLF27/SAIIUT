from config import get_db_connection


def get_all_admins():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM admins")
            admins = cursor.fetchall()
        conn.close()
        return admins
    except Exception as e:
        print(f"Error en get_all_admins: {e}")
        return None


def get_admin_by_id(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Excluimos el campo 'password' por seguridad
            cursor.execute("SELECT * FROM admins WHERE id_admins = %s", (id,))
            admin = cursor.fetchone()
        conn.close()
        return admin
    except Exception as e:
        print(f"Error en get_admin_by_id: {e}")
        return None


def create_admin(data):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO admins (nombre, ap_P, ap_M, direccion, telefono, email, sexo, no_empleado, grado_estudios)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                ),
            )
            conn.commit()
            admin_id = cursor.lastrowid
        conn.close()
        return {"id": admin_id, **data}
    except Exception as e:
        print(f"Error en create_admin: {e}")
        return None


def update_admin(id, data):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
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
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error en update_admin: {e}")
        return False


def delete_admin(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM admins WHERE id_admins = %s", (id,))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error en delete_admin: {e}")
        return False
