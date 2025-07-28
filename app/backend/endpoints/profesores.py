from flask import Blueprint, request, jsonify
import services.profesor_service as profesor_service

profesores_bp = Blueprint("profesores", __name__)


# Ruta para obtener todos los profesores
@profesores_bp.route("/todos", methods=["GET"])
def get_profesores():
    try:
        profesores = profesor_service.get_all_profesores()
        if profesores is not None:
            return jsonify(profesores), 200
        else:
            return jsonify({"error": "Error al obtener los profesores"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para obtener un profesor por ID
@profesores_bp.route("/buscar/<int:id>", methods=["GET"])
def get_profesor(id):
    try:
        profesor = profesor_service.get_profesor_by_id(id)
        if profesor:
            return jsonify(profesor), 200
        else:
            return jsonify({"error": "Profesor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para insertar un nuevo profesor
@profesores_bp.route("/insertar", methods=["POST"])
def create_profesor():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
   
    try:
        nuevo_profesor = profesor_service.create_profesor(data)
        if nuevo_profesor:
            nuevo_profesor["message"] = "Profesor creado exitosamente"
            return jsonify(nuevo_profesor), 201
        else:
            return jsonify({"error": "Error al crear el profesor"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para actualizar un profesor
@profesores_bp.route("/editar/<int:id>", methods=["PUT"])
def update_profesor(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    try:
        actualizado = profesor_service.update_profesor(id, data)
        if actualizado:
            profesor_actualizado = profesor_service.get_profesor_by_id(id)
            return jsonify(profesor_actualizado), 200
        else:
            return (
                jsonify(
                    {
                        "error": "Profesor no encontrado o los datos enviados son idénticos a los existentes"
                    }
                ),
                404,
            )
    except Exception as e:
        print(f"Error no esperado en update_profesor: {e}")
        return jsonify({"error": "Ocurrió un error interno en el servidor"}), 500


# Ruta para eliminar un profesor
@profesores_bp.route("/eliminar/<int:id>", methods=["DELETE"])
def delete_profesor(id):
    try:
        eliminado = profesor_service.delete_profesor(id)
        if eliminado:
            return jsonify({"result": "Profesor eliminado correctamente"}), 200
        else:
            return jsonify({"error": "Error al eliminar o profesor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
