from flask import Blueprint, jsonify, request

import services.alumno_service as alumno_service
from utils.validators import validate_alumno_data

alumnos_bp = Blueprint("alumnos", __name__)


@alumnos_bp.route("/todos", methods=["GET"])
def get_alumnos():
    try:
        filtros = {
            "nombre": request.args.get("nombre"),
            "apellido": request.args.get("apellido"),
            "matricula": request.args.get("matricula"),
            "carrera": request.args.get("carrera"),
        }
        filtros = {k: v for k, v in filtros.items() if v}
        alumnos = alumno_service.get_all_alumnos(filtros)
        if alumnos is not None:
            return jsonify(alumnos), 200
        else:
            return jsonify({"error": "Error al obtener los alumnos"}), 500
    except Exception as e:
        return jsonify({"error": f"Un error ocurrió: {str(e)}"}), 500


@alumnos_bp.route("/buscar/<int:id>", methods=["GET"])
def get_alumno(id):
    try:
        alumno = alumno_service.get_alumno_by_id(id)
        if alumno:
            return jsonify(alumno), 200
        else:
            return jsonify({"error": "Alumno no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alumnos_bp.route("/insertar", methods=["POST"])
def create_alumno_completo():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    errors = validate_alumno_data(data)
    if errors:
        return jsonify({'error': 'Datos inválidos', 'details': errors}), 400

    try:
        nuevo_alumno, temp_password = alumno_service.create_alumno(data)
        
        if nuevo_alumno:
            # --- SIMULACIÓN DE ENVÍO DE EMAIL ---
            # En un futuro, aquí iría la lógica para enviar el email.
            # Por ahora, lo imprimimos en la consola para poder probar.
            print(f"Usuario creado: {nuevo_alumno['matricula']}, Contraseña temporal: {temp_password}", flush=True)
            
            nuevo_alumno["message"] = "Alumno creado exitosamente. Se ha generado una contraseña temporal."
            return jsonify(nuevo_alumno), 201
        else:
            return jsonify({"error": "Error al crear el alumno"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alumnos_bp.route("/editar/<int:id>", methods=["PUT"])
def update_alumno_completo(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    # --- PASO DE VALIDACIÓN (REUTILIZADO)
    errors = validate_alumno_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400

    try:
        actualizado = alumno_service.update_alumno(id, data)
        if actualizado:
            alumno_actualizado = alumno_service.get_alumno_by_id(id)
            return jsonify(alumno_actualizado), 200
        else:
            return jsonify({"error": "Alumno no encontrado o datos sin cambios"}), 404
    except Exception as e:
        return jsonify({"error": f"Un error ocurrió: {str(e)}"}), 500


@alumnos_bp.route("/eliminar/<int:id>", methods=["DELETE"])
def delete_alumno(id):
    try:
        eliminado = alumno_service.delete_alumno(id)
        if eliminado:
            return jsonify({"result": "Alumno eliminado correctamente"}), 200
        else:
            return jsonify({"error": "Error al eliminar o alumno no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500