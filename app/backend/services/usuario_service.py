import os
import secrets
import string
from werkzeug.utils import secure_filename
from flask import current_app

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
    # Busca en la tabla de administradores
    cursor.execute("SELECT a.*, u.usuario FROM admins a JOIN usuarios u ON a.id_usuario = u.id_usuario WHERE a.id_usuario = %s", (user_id,))
    profile = cursor.fetchone()
    if profile:
        return {"role": "admin", "profile": dict(profile)}

    # Busca en la tabla de profesores
    cursor.execute("SELECT p.*, u.usuario FROM profesores p JOIN usuarios u ON p.id_usuario = u.id_usuario WHERE p.id_usuario = %s", (user_id,))
    profile = cursor.fetchone()
    if profile:
        return {"role": "profesor", "profile": dict(profile)}

    # Busca en la tabla de alumnos
    cursor.execute("SELECT al.*, u.usuario FROM alumnos al JOIN usuarios u ON al.id_usuario = u.id_usuario WHERE al.id_usuario = %s", (user_id,))
    profile = cursor.fetchone()
    if profile:
        return {"role": "alumno", "profile": dict(profile)}

    return None

@with_db_connection
def update_my_profile(cursor, user_id, role, data):
    # Actualizar campos en la tabla de rol (admins, profesores, etc.)
    allowed_fields = ['email', 'telefono'] # foto_url se maneja por separado
    fields_to_update = {k: v for k, v in data.items() if k in allowed_fields and v is not None}

    if fields_to_update:
        table_name = f"{role}s"
        if role == 'profesor':
            table_name = 'profesores'
            
        set_clause = ", ".join([f"{key} = %s" for key in fields_to_update.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE id_usuario = %s"
        
        values = list(fields_to_update.values()) + [user_id]
        cursor.execute(sql, tuple(values))

    # Actualizar la contraseña si se proporcionó una nueva
    if 'new_password' in data and data['new_password']:
        new_encrypted_pass = encrypt_password(data['new_password'])
        cursor.execute(
            "UPDATE usuarios SET contraseña = %s WHERE id_usuario = %s",
            (new_encrypted_pass, user_id)
        )

    # Devolver los datos actualizados
    return find_user_role(user_id=user_id)

@with_db_connection
def update_my_photo(cursor, user_id, role, file):
    # 1. Guardar el archivo de forma segura
    filename = secure_filename(file.filename)
    # Crear un nombre de archivo único para evitar colisiones
    unique_filename = f"{user_id}_{role}_{filename}"
    
    # Ruta de guardado
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True) # Crear carpeta si no existe
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)

    # 2. Actualizar la base de datos con la URL del archivo
    file_url = f"/static/uploads/{unique_filename}"
    table_name = f"{role}s"
    if role == 'profesor':
        table_name = 'profesores'

    sql = f"UPDATE {table_name} SET foto_url = %s WHERE id_usuario = %s"
    cursor.execute(sql, (file_url, user_id))

    # 3. Devolver el perfil actualizado
    return find_user_role(user_id=user_id)
