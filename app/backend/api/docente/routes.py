from flask import Blueprint, jsonify
import services.docente_service as docente_service

docente_bp = Blueprint('docente_api', __name__)

@docente_bp.route("/grupos/<int:id_grupo>/materias/<int:id_materia>/alumnos", methods=['GET'])
def get_alumnos_por_grupo_y_materia(id_grupo, id_materia):
    try:
        alumnos = docente_service.get_alumnos_for_calificacion(id_grupo, id_materia)
        return jsonify(alumnos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
