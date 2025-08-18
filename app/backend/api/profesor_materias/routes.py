from flask import Blueprint, jsonify, request
import services.profesor_materia_service as pm_service

# Este Blueprint se creará pero se registrará anidadamente en profesores y materias
profesor_materias_bp = Blueprint("profesor_materias", __name__)

# --- Rutas para Profesores ---

@profesor_materias_bp.route("/profesores/<int:id_profesor>/materias", methods=["GET"])
def get_materias_de_profesor(id_profesor):
    try:
        materias = pm_service.obtener_materias_de_profesor(id_profesor)
        return jsonify(materias), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@profesor_materias_bp.route("/profesores/<int:id_profesor>/materias", methods=["POST"])
def asignar_materia_a_profesor(id_profesor):
    data = request.get_json()
    id_materia = data.get("id_materia")
    if not id_materia:
        return jsonify({"error": "Se requiere 'id_materia'"}), 400
    
    try:
        pm_service.asignar_materia_a_profesor(id_profesor, id_materia)
        return jsonify({"message": "Asignación creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@profesor_materias_bp.route("/profesores/<int:id_profesor>/materias/<int:id_materia>", methods=["DELETE"])
def quitar_materia_a_profesor(id_profesor, id_materia):
    try:
        eliminado = pm_service.quitar_materia_a_profesor(id_profesor, id_materia)
        if eliminado:
            return jsonify({"message": "Asignación eliminada exitosamente"}), 200
        else:
            return jsonify({"error": "Asignación no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Rutas para Materias ---

@profesor_materias_bp.route("/materias/<int:id_materia>/profesores", methods=["GET"])
def get_profesores_de_materia(id_materia):
    try:
        profesores = pm_service.obtener_profesores_de_materia(id_materia)
        return jsonify(profesores), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
