from flask import Blueprint, jsonify, request
import services.inscripcion_service as inscripcion_service

inscripciones_bp = Blueprint("inscripciones", __name__)

@inscripciones_bp.route("/", methods=["POST"])
def inscribir_alumno():
    data = request.get_json()
    id_alumno = data.get("id_alumno")
    id_grupo = data.get("id_grupo")

    if not id_alumno or not id_grupo:
        return jsonify({"error": "Se requiere 'id_alumno' y 'id_grupo'"}), 400

    try:
        resultado = inscripcion_service.inscribir_alumno_en_grupo(id_alumno, id_grupo)
        return jsonify(resultado), 201
    except inscripcion_service.InscripcionError as e:
        return jsonify({"error": str(e)}), 409  # Conflict, ya que es un error de negocio
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@inscripciones_bp.route("/alumnos/<int:id_alumno>", methods=["GET"])
def get_inscripciones_de_alumno(id_alumno):
    # Opcionalmente, filtrar por periodo si se pasa como query param
    id_periodo = request.args.get("id_periodo", type=int)
    try:
        inscripciones = inscripcion_service.obtener_inscripciones_de_alumno(id_alumno, id_periodo)
        return jsonify(inscripciones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
