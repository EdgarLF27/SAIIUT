from flask import Blueprint, jsonify, request
import services.docente_service as docente_service
import services.periodo_service as periodo_service

docente_bp = Blueprint("docente", __name__)

@docente_bp.route("/<int:id_profesor>/grupos", methods=["GET"])
def get_grupos_materias_route(id_profesor):
    # Intentar obtener el periodo activo. Si no, el frontend deberá proveerlo.
    id_periodo = request.args.get("id_periodo", type=int)
    if not id_periodo:
        # Lógica para autodetectar el periodo activo (a implementar si se desea)
        return jsonify({"error": "Se requiere un 'id_periodo' como query param."}), 400
    
    try:
        data = docente_service.get_grupos_y_materias_de_profesor(id_profesor, id_periodo)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@docente_bp.route("/<int:id_profesor>/grupos/<int:id_grupo>/materias/<int:id_materia>/alumnos", methods=["GET"])
def get_alumnos_calificaciones_route(id_profesor, id_grupo, id_materia):
    try:
        alumnos = docente_service.get_alumnos_con_calificaciones(id_profesor, id_grupo, id_materia)
        return jsonify(alumnos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@docente_bp.route("/calificaciones/<int:id_calificacion>", methods=["PUT"])
def update_calificacion_route(id_calificacion):
    data = request.get_json()
    parcial = data.get("parcial")
    calificacion = data.get("calificacion")

    if not parcial or calificacion is None:
        return jsonify({"error": "Se requiere 'parcial' y 'calificacion'"}), 400

    try:
        actualizado = docente_service.actualizar_calificacion(id_calificacion, parcial, calificacion)
        if actualizado:
            return jsonify({"message": "Calificación actualizada exitosamente"}), 200
        else:
            return jsonify({"error": "No se encontró el registro de calificación"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
