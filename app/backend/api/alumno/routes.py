from flask import Blueprint, jsonify, request
import services.inscripcion_service as inscripcion_service

alumno_bp = Blueprint("alumno", __name__)

@alumno_bp.route("/<int:id_alumno>/calificaciones", methods=["GET"])
def get_calificaciones_de_alumno(id_alumno):
    try:
        # Se llama al servicio sin el parámetro de periodo
        calificaciones = inscripcion_service.obtener_inscripciones_de_alumno(id_alumno)
        return jsonify(calificaciones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
