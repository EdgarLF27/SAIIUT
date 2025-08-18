from flask import Blueprint, jsonify, request

import services.profesor_service as profesor_service
from utils.validators import validate_profesor_data

profesores_bp = Blueprint("profesores", __name__)


@profesores_bp.route("/", methods=["GET"])
def get_profesores():
    try:
        filtros = {"nombre": request.args.get("nombre")}
        filtros = {k: v for k, v in filtros.items() if v}
        profesores = profesor_service.get_all_profesores(filtros)
        if profesores is not None:
            return jsonify(profesores), 200
        else:
            return jsonify({"error": "Error al obtener los profesores"}), 500
    except Exception as e:
        return jsonify({"error": f"Un error ocurrió: {str(e)}"}), 500


@profesores_bp.route("/<int:id>", methods=["GET"])
def get_profesor(id):
    try:
        profesor = profesor_service.get_profesor_by_id(id)
        if profesor:
            return jsonify(profesor), 200
        else:
            return jsonify({"error": "Profesor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@profesores_bp.route("/", methods=["POST"])
def create_profesor():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    errors = validate_profesor_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400

    try:
        nuevo_profesor, temp_password = profesor_service.create_profesor(data)
        if nuevo_profesor:
            print(
                f"Usuario de Profesor creado: {nuevo_profesor['no_empleado']}, Contraseña temporal: {temp_password}",
                flush=True,
            )
            nuevo_profesor["message"] = "Profesor creado exitosamente"
            return jsonify(nuevo_profesor), 201
        else:
            return jsonify({"error": "Error al crear el profesor"}), 500
    except Exception as e:
        # (Opcional) Podríamos añadir traceback aquí también para mejor depuración
        return jsonify({"error": str(e)}), 500


@profesores_bp.route("/<int:id>", methods=["PUT"])
def update_profesor(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    errors = validate_profesor_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400

    try:
        actualizado = profesor_service.update_profesor(id, data)
        if actualizado:
            profesor_actualizado = profesor_service.get_profesor_by_id(id)
            return jsonify(profesor_actualizado), 200
        else:
            return jsonify({"error": "Profesor no encontrado o datos sin cambios"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@profesores_bp.route("/<int:id>", methods=["DELETE"])
def delete_profesor(id):
    try:
        eliminado = profesor_service.delete_profesor(id)
        if eliminado:
            return jsonify({"result": "Profesor eliminado correctamente"}), 200
        else:
            return jsonify({"error": "Error al eliminar o profesor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
