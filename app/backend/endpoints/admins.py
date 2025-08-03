from flask import Blueprint, jsonify, request

import services.admin_service as admin_service

admins_bp = Blueprint("admins", __name__)


# Obtener todos los admins
@admins_bp.route("/todos", methods=["GET"])
def get_admins():
    try:
        filtros = {"nombre": request.args.get("nombre")}
        filtros = {k: v for k, v in filtros.items() if v}

        admins = admin_service.get_all_admins(filtros)
        if admins is not None:
            return jsonify(admins), 200
        else:
            return jsonify({"error": "Error al obtener los administradores"}), 500
    except Exception as e:
        return jsonify({"error": f"Un error ocurrió: {str(e)}"}), 500


# Obtener un admin por ID
@admins_bp.route("/buscar/<int:id>", methods=["GET"])
def get_admin(id):
    try:
        admin = admin_service.get_admin_by_id(id)
        if admin:
            return jsonify(admin), 200
        else:
            return jsonify({"error": "Admin no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Crear un nuevo admin
@admins_bp.route("/insertar", methods=["POST"])
def create_admin():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    try:
        nuevo_admin = admin_service.create_admin(data)
        if nuevo_admin:
            nuevo_admin["message"] = "Administrador creado exitosamente"
            return jsonify(nuevo_admin), 201
        else:
            return jsonify({"error": "Error al crear el administrador"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Actualizar un admin
@admins_bp.route("/editar/<int:id>", methods=["PUT"])
def update_admin(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    try:
        actualizado = admin_service.update_admin(id, data)
        if actualizado:
            admin_actualizado = admin_service.get_admin_by_id(id)
            return jsonify(admin_actualizado), 200
        else:
            return (
                jsonify({"error": "Error al actualizar o administrador no encontrado"}),
                404,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Eliminar un admin
@admins_bp.route("/eliminar/<int:id>", methods=["DELETE"])
def delete_admin(id):
    try:
        eliminado = admin_service.delete_admin(id)
        if eliminado:
            return jsonify({"result": "Admin eliminado correctamente"}), 200
        else:
            return (
                jsonify({"error": "Error al eliminar o administrador no encontrado"}),
                404,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
