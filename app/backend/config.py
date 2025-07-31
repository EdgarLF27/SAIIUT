import pymysql
import os
from dotenv import load_dotenv
from functools import wraps #importacion de decoradores

load_dotenv("credentials.env")

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "cursorclass": pymysql.cursors.DictCursor,
}


def get_db_connection():
    return pymysql.connect(**db_config)


def with_db_connection(fn): #decorador para manejar la conexion a la base de datos, después de ahi se pasa la función que lo vaya a usar

    @wraps(fn)
    def wrapper(*args, **kwargs):
        conn = None
        # Determina si es una operación de escritura por el nombre de la función
        is_write_operation = any(
            keyword in fn.__name__ for keyword in ["create", "update", "delete"]
        )

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Pasa el cursor como primer argumento a la función original
                result = fn(cursor, *args, **kwargs)

                # Si es una operación de escritura, haz commit
                if is_write_operation:
                    conn.commit()

                return result
        except pymysql.MySQLError as e:
            print(f"Error de base de datos en '{fn.__name__}': {e}")
            if conn and is_write_operation:
                conn.rollback()
            # Relanzamos la excepción para que la capa de servicio la maneje si es necesario
            raise e
        except Exception as e:
            print(f"Error inesperado en '{fn.__name__}': {e}")
            if conn and is_write_operation:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    return wrapper