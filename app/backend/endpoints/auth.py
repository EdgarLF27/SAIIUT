from flask import Blueprint, jsonify, request
import services.usuario_service as usuario_service

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()
    if not data or not data.get("usuario") or not data.get("contraseña"):
        return jsonify({"success": False, "error": "Faltan usuario o contraseña"}), 400

    # --- Verificación del usuario ---
    # Llamamos al servicio para verificar si el usuario y la contraseña son correctos.
    user = usuario_service.verify_user(data["usuario"], data["contraseña"])

    if not user:
        return jsonify({"success": False, "error": "Credenciales incorrectas"}), 401

    # --- Búsqueda del rol ---
    # Si el usuario es válido, buscamos su rol y perfil en las tablas correspondientes.
    role_info = usuario_service.find_user_role(user["id_usuario"])

    if not role_info:
        return (
            jsonify(
                {"success": False, "error": "Usuario válido pero sin rol asignado"}
            ),
            500,
        )

    # --- Respuesta exitosa ---
    # Devolvemos éxito, el rol y los datos del perfil para que el frontend pueda redirigir.
    return (
        jsonify(
            {
                "success": True,
                "role": role_info["role"],
                "user_data": role_info["profile"],
            }
        ),
        200,
    )
