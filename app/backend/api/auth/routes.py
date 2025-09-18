from flask import Blueprint, jsonify, request, session
import services.usuario_service as usuario_service

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("usuario") or not data.get("contraseña"):
        return jsonify({"success": False, "error": "Faltan usuario o contraseña"}), 400

    user = usuario_service.verify_user(data["usuario"], data["contraseña"])
    if not user:
        return jsonify({"success": False, "error": "Credenciales incorrectas"}), 401

    role_info = usuario_service.find_user_role(user["id_usuario"])
    if not role_info:
        return jsonify({"success": False, "error": "Usuario válido pero sin rol asignado"}), 500

    # Guardar en la sesión
    session['user_id'] = user["id_usuario"]
    session['user_role'] = role_info["role"]
    
    print(f"--- LOGIN OK ---\nUser ID: {session['user_id']}, Role: {session['user_role']}\nSession object en servidor: {session}\n----------------", flush=True)

    return jsonify({
        "success": True,
        "role": role_info["role"],
        "user_data": role_info["profile"],
    }), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Sesión cerrada exitosamente"}), 200

@auth_bp.route("/me", methods=["GET"])
def get_me():
    print(f"--- GET /ME ---\nHeaders: {request.headers}Session object en servidor: {session}\n----------------", flush=True)
    if 'user_id' not in session:
        print("Acceso a /me DENEGADO. No se encontró user_id en la sesión.", flush=True)
        return jsonify({"error": "No autorizado"}), 401
    
    user_id = session['user_id']
    print(f"Acceso a /me PERMITIDO. User ID: {user_id}", flush=True)
    user_info = usuario_service.find_user_role(user_id)
    
    if not user_info:
        return jsonify({"error": "Usuario no encontrado"}), 404
        
    return jsonify(user_info), 200

@auth_bp.route("/me", methods=["PUT"])
def update_me():
    if 'user_id' not in session:
        return jsonify({"error": "No autorizado"}), 401

    user_id = session['user_id']
    role = session['user_role']
    data = request.get_json()

    try:
        updated_user = usuario_service.update_my_profile(user_id, role, data)
        return jsonify(updated_user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/me/photo", methods=["POST"])
def upload_my_photo():
    if 'user_id' not in session:
        return jsonify({"error": "No autorizado"}), 401

    user_id = session['user_id']
    role = session['user_role']

    if 'profile_photo' not in request.files:
        return jsonify({"error": "No se encontró el archivo de imagen"}), 400

    file = request.files['profile_photo']
    if file.filename == '':
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400

    try:
        updated_user = usuario_service.update_my_photo(user_id, role, file)
        return jsonify(updated_user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
