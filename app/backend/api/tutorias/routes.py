from flask import Blueprint, jsonify, request
import services.tutoria_service as tutoria_service

tutorias_bp = Blueprint("tutorias", __name__)

@tutorias_bp.route("/", methods=["POST"])
def asignar_tutor():
    data = request.get_json()
    id_profesor = data.get("id_profesor")
    id_grupo = data.get("id_grupo")

    if not id_profesor or not id_grupo:
        return jsonify({"error": "Se requiere 'id_profesor' y 'id_grupo'"}), 400

    try:
        asignacion = tutoria_service.asignar_tutor_a_grupo(id_profesor, id_grupo)
        return jsonify(asignacion), 201
    except tutoria_service.TutoriaError as e:
        return jsonify({"error": str(e)}), 409  # 409 Conflict es bueno para duplicados
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tutorias_bp.route("/grupo/<int:id_grupo>", methods=["GET"])
def get_tutor_de_grupo(id_grupo):
    try:
        tutor = tutoria_service.obtener_tutor_de_grupo(id_grupo)
        if tutor:
            return jsonify(tutor), 200
        return jsonify({"message": "Este grupo no tiene un tutor asignado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tutorias_bp.route("/profesor/<int:id_profesor>", methods=["GET"])
def get_grupos_de_tutor(id_profesor):
    try:
        grupos = tutoria_service.obtener_grupos_de_tutor(id_profesor)
        return jsonify(grupos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tutorias_bp.route("/grupo/<int:id_grupo>", methods=["DELETE"])
def quitar_tutor_de_grupo(id_grupo):
    try:
        eliminado = tutoria_service.quitar_asignacion_tutor(id_grupo)
        if eliminado:
            return jsonify({"message": "Asignación de tutoría eliminada exitosamente"}), 200
        else:
            return jsonify({"error": "No se encontró asignación de tutoría para este grupo"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
