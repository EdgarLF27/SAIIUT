from flask import Blueprint, jsonify, request
import services.grupo_service as grupo_service
from utils.validators import validate_grupo_data

grupos_bp = Blueprint("grupos", __name__)

@grupos_bp.route("/", methods=["GET"])
def get_grupos():
    try:
        grupos = grupo_service.get_all_grupos()
        return jsonify(grupos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@grupos_bp.route("/<int:id>", methods=["GET"])
def get_grupo(id):
    try:
        grupo = grupo_service.get_grupo_by_id(id)
        if grupo:
            return jsonify(grupo), 200
        else:
            return jsonify({"error": "Grupo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@grupos_bp.route("/", methods=["POST"])
def create_grupo():
    data = request.get_json()
    errors = validate_grupo_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    try:
        nuevo_grupo = grupo_service.create_grupo(data)
        return jsonify(nuevo_grupo), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@grupos_bp.route("/<int:id>", methods=["PUT"])
def update_grupo(id):
    data = request.get_json()
    errors = validate_grupo_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400

    try:
        actualizado = grupo_service.update_grupo(id, data)
        if actualizado:
            return jsonify({"message": "Grupo actualizado exitosamente"}), 200
        else:
            return jsonify({"error": "Grupo no encontrado o datos sin cambios"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@grupos_bp.route("/<int:id>", methods=["DELETE"])
def delete_grupo(id):
    try:
        eliminado = grupo_service.delete_grupo(id)
        if eliminado:
            return jsonify({"message": "Grupo eliminado exitosamente"}), 200
        else:
            return jsonify({"error": "Grupo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
