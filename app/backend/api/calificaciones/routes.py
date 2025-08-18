from flask import Blueprint, jsonify, request
import services.calificacion_service as calificacion_service
from utils.validators import validate_calificacion_data

calificaciones_bp = Blueprint("calificaciones", __name__)

@calificaciones_bp.route("/", methods=["GET"])
def get_calificaciones():
    try:
        calificaciones = calificacion_service.get_all_calificaciones()
        return jsonify(calificaciones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@calificaciones_bp.route("/<int:id>", methods=["GET"])
def get_calificacion(id):
    try:
        calificacion = calificacion_service.get_calificacion_by_id(id)
        if calificacion:
            return jsonify(calificacion), 200
        else:
            return jsonify({"error": "Calificación no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@calificaciones_bp.route("/", methods=["POST"])
def create_calificacion():
    data = request.get_json()
    errors = validate_calificacion_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    try:
        nueva_calificacion = calificacion_service.create_calificacion(data)
        return jsonify(nueva_calificacion), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@calificaciones_bp.route("/<int:id>", methods=["PUT"])
def update_calificacion(id):
    data = request.get_json()
    errors = validate_calificacion_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400

    try:
        actualizado = calificacion_service.update_calificacion(id, data)
        if actualizado:
            return jsonify({"message": "Calificación actualizada exitosamente"}), 200
        else:
            return jsonify({"error": "Calificación no encontrada o datos sin cambios"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@calificaciones_bp.route("/<int:id>", methods=["DELETE"])
def delete_calificacion(id):
    try:
        eliminado = calificacion_service.delete_calificacion(id)
        if eliminado:
            return jsonify({"message": "Calificación eliminada exitosamente"}), 200
        else:
            return jsonify({"error": "Calificación no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
