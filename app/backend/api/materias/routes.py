from flask import Blueprint, jsonify, request
import services.materia_service as materia_service
from utils.validators import validate_materia_data

materias_bp = Blueprint("materias", __name__)

@materias_bp.route("/", methods=["GET"])
def get_materias():
    try:
        materias = materia_service.get_all_materias()
        return jsonify(materias), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@materias_bp.route("/<int:id>", methods=["GET"])
def get_materia(id):
    try:
        materia = materia_service.get_materia_by_id(id)
        if materia:
            return jsonify(materia), 200
        else:
            return jsonify({"error": "Materia no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@materias_bp.route("/", methods=["POST"])
def create_materia():
    data = request.get_json()
    errors = validate_materia_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    try:
        nueva_materia = materia_service.create_materia(data)
        return jsonify(nueva_materia), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@materias_bp.route("/<int:id>", methods=["PUT"])
def update_materia(id):
    data = request.get_json()
    errors = validate_materia_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400

    try:
        actualizado = materia_service.update_materia(id, data)
        if actualizado:
            return jsonify({"message": "Materia actualizada exitosamente"}), 200
        else:
            return jsonify({"error": "Materia no encontrada o datos sin cambios"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@materias_bp.route("/<int:id>", methods=["DELETE"])
def delete_materia(id):
    try:
        eliminado = materia_service.delete_materia(id)
        if eliminado:
            return jsonify({"message": "Materia eliminada exitosamente"}), 200
        else:
            return jsonify({"error": "Materia no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
