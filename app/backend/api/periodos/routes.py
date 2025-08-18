from flask import Blueprint, jsonify, request
import services.periodo_service as periodo_service
from utils.validators import validate_periodo_data

periodos_bp = Blueprint("periodos", __name__)

@periodos_bp.route("/", methods=["GET"])
def get_periodos():
    try:
        periodos = periodo_service.get_all_periodos()
        return jsonify(periodos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@periodos_bp.route("/<int:id>", methods=["GET"])
def get_periodo(id):
    try:
        periodo = periodo_service.get_periodo_by_id(id)
        if periodo:
            return jsonify(periodo), 200
        else:
            return jsonify({"error": "Periodo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@periodos_bp.route("/", methods=["POST"])
def create_periodo():
    data = request.get_json()
    errors = validate_periodo_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    try:
        nuevo_periodo = periodo_service.create_periodo(data)
        return jsonify(nuevo_periodo), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@periodos_bp.route("/<int:id>", methods=["PUT"])
def update_periodo(id):
    data = request.get_json()
    errors = validate_periodo_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400

    try:
        actualizado = periodo_service.update_periodo(id, data)
        if actualizado:
            return jsonify({"message": "Periodo actualizado exitosamente"}), 200
        else:
            return jsonify({"error": "Periodo no encontrado o datos sin cambios"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@periodos_bp.route("/<int:id>", methods=["DELETE"])
def delete_periodo(id):
    try:
        eliminado = periodo_service.delete_periodo(id)
        if eliminado:
            return jsonify({"message": "Periodo eliminado exitosamente"}), 200
        else:
            return jsonify({"error": "Periodo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
