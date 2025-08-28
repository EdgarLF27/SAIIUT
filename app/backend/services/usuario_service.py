import os
import secrets
import string

from cryptography.fernet import Fernet

from config import with_db_connection

# Carga la clave de encriptación desde el entorno.
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# Si la clave no se encuentra, el programa debe detenerse para evitar inconsistencias.
if not ENCRYPTION_KEY:
    raise ValueError(
        "Error crítico: La variable de entorno ENCRYPTION_KEY no está definida en credentials.env"
    )

# Convertimos la clave a bytes para usarla en la encriptación
cipher_suite = Fernet(ENCRYPTION_KEY.encode("utf-8"))


# Genera una contraseña al azar
def generate_random_password(length=10):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(length))


# Encripta la contraseña
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode("utf-8"))


# Desencripta la contraseña
def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode("utf-8")


# Versión Interna (Requiere un cursor
def _create_user_and_get_id_internal(cursor, username):
    cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:

        return existing_user["id_usuario"], None
    plain_password = generate_random_password()
    encrypted_pass = encrypt_password(plain_password)

    sql = "INSERT INTO usuarios (usuario, contraseña) VALUES (%s, %s) RETURNING id_usuario;"
    cursor.execute(sql, (username, encrypted_pass))

    user_id = cursor.fetchone()["id_usuario"]
    return user_id, plain_password


# --- Versión Externa: Maneja la conexión con el decorador ---
@with_db_connection
def create_user_and_get_id(cursor, username):
    """Versión pública que maneja su propia conexión."""
    return _create_user_and_get_id_internal(cursor, username)


@with_db_connection
def verify_user(cursor, username, plain_password):
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (username,))
    user = cursor.fetchone()
    if user:
        # La columna BYTEA de la BD se lee como un objeto 'memoryview'.
        # Lo convertimos explícitamente a 'bytes' para que la librería de criptografía lo acepte.
        encrypted_pass_bytes = bytes(user["contraseña"])
        decrypted_pass = decrypt_password(encrypted_pass_bytes)
        if decrypted_pass == plain_password:
            return user
    return None


@with_db_connection
def find_user_role(cursor, user_id):
    # ... (el resto de la función se mantiene igual)
    cursor.execute("SELECT * FROM alumnos WHERE id_usuario = %s", (user_id,))
    profile = cursor.fetchone()
    if profile:
        return {"role": "alumno", "profile": profile}
    cursor.execute("SELECT * FROM profesores WHERE id_usuario = %s", (user_id,))
    profile = cursor.fetchone()
    if profile:
        return {"role": "profesor", "profile": profile}
    cursor.execute("SELECT * FROM admins WHERE id_usuario = %s", (user_id,))
    profile = cursor.fetchone()
    if profile:
        return {"role": "admin", "profile": profile}
    return None
