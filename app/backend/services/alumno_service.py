from config import get_db_connection


def get_all_alumnos():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos")
            alumnos = cursor.fetchall()
        conn.close()
        return alumnos
    except Exception as e:
        print(f"Error en get_all_alumnos: {e}")
        return None


def get_alumno_by_id(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos WHERE id_alumno = %s", (id,))
            alumno = cursor.fetchone()
        conn.close()
        return alumno
    except Exception as e:
        print(f"Error en get_alumno_by_id: {e}")
        return None


def create_alumno(data):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO alumnos (nombre, ap_P, ap_M, matricula, telefono, email, carrera, grado, grupo, sexo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                    data["carrera"],
                    data["grado"],
                    data["grupo"],
                    data["sexo"],
                ),
            )
            conn.commit()
            alumno_id = cursor.lastrowid
        conn.close()
        return {"id": alumno_id, **data}
    except Exception as e:
        print(f"Error en create_alumno: {e}")
        return None


def update_alumno(id, data):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            UPDATE alumnos
            SET nombre=%s, ap_P=%s, ap_M=%s, matricula=%s, telefono=%s, email=%s, carrera=%s, grado=%s, grupo=%s, sexo=%s
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
                    data["carrera"],
                    data["grado"],
                    data["grupo"],
                    data["sexo"],
                    id,
                ),
            )
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en update_alumno: {e}")
        return False


def delete_alumno(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM alumnos WHERE id_alumno = %s", (id,))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en delete_alumno: {e}")
        return False
