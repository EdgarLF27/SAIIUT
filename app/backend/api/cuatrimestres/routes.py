from flask import Blueprint, jsonify, request
import services.cuatrimestre_service as cuatrimestre_service

cuatrimestres_bp = Blueprint("cuatrimestres", __name__)

@cuatrimestres_bp.route("/", methods=["GET"])
def get_cuatrimestres():
    try:
        cuatrimestres = cuatrimestre_service.get_all_cuatrimestres()
        return jsonify(cuatrimestres), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cuatrimestres_bp.route("/<int:id>", methods=["GET"])
def get_cuatrimestre(id):
    try:
        cuatrimestre = cuatrimestre_service.get_cuatrimestre_by_id(id)
        if cuatrimestre:
            return jsonify(cuatrimestre), 200
        else:
            return jsonify({"error": "Cuatrimestre no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cuatrimestres_bp.route("/", methods=["POST"])
def create_cuatrimestre():
    data = request.get_json()
    # Aquí podrías añadir validaciones si fueran necesarias
    if not data or not data.get('nombre') or not data.get('orden'):
        return jsonify({"error": "Datos incompletos. Se requiere 'nombre' y 'orden'."}), 400
    
    try:
        nuevo_cuatrimestre = cuatrimestre_service.create_cuatrimestre(data)
        return jsonify(nuevo_cuatrimestre), 201
    except Exception as e:
        # Podríamos manejar errores específicos, como 'orden' duplicado
        return jsonify({"error": str(e)}), 500

@cuatrimestres_bp.route("/<int:id>", methods=["PUT"])
def update_cuatrimestre(id):
    data = request.get_json()
    if not data or not data.get('nombre') or not data.get('orden'):
        return jsonify({"error": "Datos incompletos. Se requiere 'nombre' y 'orden'."}), 400

    try:
        actualizado = cuatrimestre_service.update_cuatrimestre(id, data)
        if actualizado:
            return jsonify({"message": "Cuatrimestre actualizado exitosamente"}), 200
        else:
            return jsonify({"error": "Cuatrimestre no encontrado o datos sin cambios"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cuatrimestres_bp.route("/<int:id>", methods=["DELETE"])
def delete_cuatrimestre(id):
    try:
        eliminado = cuatrimestre_service.delete_cuatrimestre(id)
        if eliminado:
            return jsonify({"message": "Cuatrimestre eliminado exitosamente"}), 200
        else:
            return jsonify({"error": "Cuatrimestre no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
