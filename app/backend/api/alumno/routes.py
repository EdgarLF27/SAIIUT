from flask import Blueprint, jsonify, request
import services.inscripcion_service as inscripcion_service

alumno_bp = Blueprint("alumno", __name__)

@alumno_bp.route("/<int:id_alumno>/calificaciones", methods=["GET"])
def get_calificaciones_de_alumno(id_alumno):
    id_periodo = request.args.get("id_periodo", type=int)
    
    # Podríamos añadir una lógica para obtener el periodo activo si no se proporciona
    if not id_periodo:
        return jsonify({"error": "Se requiere un 'id_periodo' como query param."}), 400

    try:
        # Reutilizamos el servicio que ya obtiene toda la información necesaria
        calificaciones = inscripcion_service.obtener_inscripciones_de_alumno(id_alumno, id_periodo)
        return jsonify(calificaciones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
