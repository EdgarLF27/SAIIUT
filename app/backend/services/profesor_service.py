from config import get_db_connection


def get_all_profesores():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM profesores")
            profesores = cursor.fetchall()
        conn.close()
        return profesores
    except Exception as e:
        print(f"Error en get_all_profesores: {e}")
        return None


def get_profesor_by_id(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM profesores WHERE id_profesor = %s",
                (id,),
            )
            profesor = cursor.fetchone()
        conn.close()
        return profesor
    except Exception as e:
        print(f"Error en get_profesor_by_id: {e}")
        return None


def create_profesor(data):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO profesores (nombre, ap_P, ap_M, no_empleado, telefono, email, grado_estudio, sexo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    data["nombre"],
                    data["ap_P"],
                    data["ap_M"],
                    data["no_empleado"],
                    data["telefono"],
                    data["email"],
                    data["grado_estudio"],
                    data["sexo"],
                ),
            )
            conn.commit()
            profesor_id = cursor.lastrowid
        conn.close()
        return {"id": profesor_id, **data}
    except Exception as e:
        print(f"Error en create_profesor: {e}")
        return None


def update_profesor(id, data):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            UPDATE profesores
            SET nombre=%s, ap_P=%s, ap_M=%s, no_empleado=%s, telefono=%s, email=%s, grado_estudio=%s, sexo=%s
            WHERE id_profesor=%s
            """
            cursor.execute(
                sql,
                (
                    data["nombre"],
                    data["ap_P"],
                    data["ap_M"],
                    data["no_empleado"],
                    data["telefono"],
                    data["email"],
                    data["grado_estudio"],
                    data["sexo"],
                    id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error en update_profesor: {e}")
        return False


def delete_profesor(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM profesores WHERE id_profesor = %s", (id,))
            conn.commit()

            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error en delete_profesor: {e}")
        return False
