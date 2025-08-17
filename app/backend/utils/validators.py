import re

# Herramientas de Validación Genéricas


def is_valid_email(email):
    """Verifica si el formato del email es válido."""
    if not email:
        return False
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(regex, email) is not None


def is_valid_phone(phone):
    """Verifica si el teléfono contiene solo números y tiene una longitud razonable."""
    if not phone:
        return False
    return phone.isdigit() and len(phone) == 10


# Validadores Específicos por Rol


def validate_alumno_data(data):
    """Valida los datos para crear o actualizar un alumno (versión para BD de producción)."""
    errors = []
    # Actualizamos los campos requeridos según el nuevo esquema de la BD.
    required_fields = [
        "nombre",
        "ap_P",
        "ap_M",
        "matricula",
        "email",
        "telefono",
        "sexo",
        "id_carrera",
    ]
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            errors.append(f"El campo '{field}' es obligatorio.")

    # Si faltan campos básicos, devolvemos los errores inmediatamente.
    if errors:
        return errors

    # Validaciones de formato y tipo.
    if not is_valid_email(data["email"]):
        errors.append("El formato del email no es válido.")

    # Hacemos la validación del teléfono opcional, solo si el campo existe y no está vacío.
    if data.get("telefono") and not isinstance(data.get("telefono"), str):
        errors.append("El teléfono debe ser una cadena de texto.")

    # Intentamos convertir id_carrera a entero. Si falla, añadimos un error.
    try:
        data["id_carrera"] = int(data["id_carrera"])
    except (ValueError, TypeError):
        errors.append("El campo 'id_carrera' debe ser un número entero válido.")

    if len(data["nombre"]) > 50:
        errors.append("El nombre no puede tener más de 50 caracteres.")
    if len(data["matricula"]) > 20:
        errors.append("La matrícula no puede tener más de 20 caracteres.")

    return errors


def validate_profesor_data(data):
    """Valida los datos para crear o actualizar un profesor."""
    errors = []
    required_fields = [
        "nombre",
        "ap_P",
        "ap_M",
        "telefono",
        "email",
        "no_empleado",
        "grado_estudio",
        "sexo",
    ]
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"El campo '{field}' es obligatorio.")

    if errors:
        return errors

    if not is_valid_email(data["email"]):
        errors.append("El formato del email no es válido.")
    if not is_valid_phone(data["telefono"]):
        errors.append("El teléfono solo debe contener números.")
    return errors


def validate_admin_data(data):
    """Valida los datos para crear o actualizar un administrador."""
    errors = []
    required_fields = [
        "nombre",
        "ap_P",
        "ap_M",
        "telefono",
        "email",
        "sexo",
        "no_empleado",
        "grado_estudios",
    ]
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"El campo '{field}' es obligatorio.")

    if errors:
        return errors

    if not is_valid_email(data["email"]):
        errors.append("El formato del email no es válido.")
    if not is_valid_phone(data["telefono"]):
        errors.append("El teléfono solo debe contener números.")
    return errors
