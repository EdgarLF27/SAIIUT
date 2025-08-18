import os
from functools import wraps
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

# Carga las variables de entorno (asegúrate de que tu .env tenga las credenciales de Supabase)
load_dotenv("credentials.env")

# Configuración para la conexión a PostgreSQL (Supabase)
db_config = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT"),
}


def get_db_connection():
    """Establece y devuelve una nueva conexión a la base de datos PostgreSQL."""
    return psycopg2.connect(**db_config)


def with_db_connection(fn):
    """
    Decorador para manejar de forma segura las conexiones y transacciones a la BD.
    Abre una conexión, crea un cursor, ejecuta la función y cierra la conexión.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        conn = None
        # Determina si es una operación de escritura por el nombre de la función
        is_write_operation = any(
            keyword in fn.__name__ for keyword in ["create", "update", "delete", "asignar", "quitar", "inscribir"]
        )

        try:
            conn = get_db_connection()
            # Usamos DictCursor para que las filas se devuelvan como diccionarios
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                # Pasa el cursor como primer argumento a la función original
                result = fn(cursor, *args, **kwargs)

                # Si es una operación de escritura, haz commit
                if is_write_operation:
                    conn.commit()

                return result
        except psycopg2.Error as e:
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
