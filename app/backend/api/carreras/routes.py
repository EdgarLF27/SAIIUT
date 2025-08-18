from flask import Blueprint, jsonify, request
import services.carrera_service as carrera_service
from utils.validators import validate_carrera_data

carreras_bp = Blueprint("carreras", __name__)

@carreras_bp.route("/", methods=["GET"])
def get_carreras():
    try:
        carreras = carrera_service.get_all_carreras()
        return jsonify(carreras), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@carreras_bp.route("/<int:id>", methods=["GET"])
def get_carrera(id):
    try:
        carrera = carrera_service.get_carrera_by_id(id)
        if carrera:
            return jsonify(carrera), 200
        else:
            return jsonify({"error": "Carrera no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@carreras_bp.route("/", methods=["POST"])
def create_carrera():
    data = request.get_json()
    errors = validate_carrera_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    try:
        nueva_carrera = carrera_service.create_carrera(data)
        return jsonify(nueva_carrera), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@carreras_bp.route("/<int:id>", methods=["PUT"])
def update_carrera(id):
    data = request.get_json()
    errors = validate_carrera_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400

    try:
        actualizado = carrera_service.update_carrera(id, data)
        if actualizado:
            return jsonify({"message": "Carrera actualizada exitosamente"}), 200
        else:
            return jsonify({"error": "Carrera no encontrada o datos sin cambios"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@carreras_bp.route("/<int:id>", methods=["DELETE"])
def delete_carrera(id):
    try:
        eliminado = carrera_service.delete_carrera(id)
        if eliminado:
            return jsonify({"message": "Carrera eliminada exitosamente"}), 200
        else:
            return jsonify({"error": "Carrera no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
