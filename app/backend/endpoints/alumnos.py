from flask import Blueprint, request, jsonify


import services.alumno_service as alumno_service

alumnos_bp = Blueprint("alumnos", __name__)


# Ruta para obtener todos los alumnos
@alumnos_bp.route('/todos', methods=['GET'])
def get_alumnos():
    try:
        # Recogemos los posibles filtros de los argumentos de la URL
        filtros = {
            'nombre': request.args.get('nombre'),
            'apellido': request.args.get('apellido'),
            'carrera': request.args.get('carrera'),
            'matricula': request.args.get('matricula')
        }
        # Pasamos el diccionario de filtros al servicio
        alumnos = alumno_service.get_all_alumnos(filtros)
        
        if alumnos is not None:
            return jsonify(alumnos), 200
        else:
            # Este caso ahora es menos probable, a menos que haya un error de BD
            return jsonify({'error': 'Error al obtener los alumnos'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Ruta para obtener un alumno por ID
@alumnos_bp.route("/buscar/<int:id>", methods=["GET"])
def get_alumno(id):
    try:
        # Llamamos a la función del servicio
        alumno = alumno_service.get_alumno_by_id(id)
        if alumno:
            return jsonify(alumno), 200
        else:
            return jsonify({"error": "Alumno no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para insertar un nuevo alumno
@alumnos_bp.route("/insertar", methods=["POST"])
def create_alumno_completo():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    try:
        nuevo_alumno = alumno_service.create_alumno(data)
        if nuevo_alumno:
            nuevo_alumno["message"] = "Alumno creado exitosamente"
            return jsonify(nuevo_alumno), 201
        else:
            return jsonify({"error": "Error al crear el alumno"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para actualizar un alumno
@alumnos_bp.route("/editar/<int:id>", methods=["PUT"])
def update_alumno_completo(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    # Validación de campos (para después)
    required_fields = [
        "nombre",
        "ap_P",
        "ap_M",
        "matricula",
        "telefono",
        "email",
        "carrera",
        "grado",
        "grupo",
        "sexo",
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo obligatorio: '{field}'"}), 400

    try:
        # Llamamos a la función del servicio
        actualizado = alumno_service.update_alumno(id, data)
        if actualizado:
            # Opcional: devolver el objeto actualizado
            alumno_actualizado = alumno_service.get_alumno_by_id(id)
            return jsonify(alumno_actualizado), 200
        else:
            return (
                jsonify(
                    {
                        "error": "Alumno no encontrado o los datos enviados son idénticos a los existentes"
                    }
                ),
                404,
            )
    except Exception as e:
        print(f"Error no esperado en update_alumno_completo: {e}")
        return jsonify({"error": "Ocurrió un error interno en el servidor"}), 500


# Ruta para eliminar un alumno
@alumnos_bp.route("/eliminar/<int:id>", methods=["DELETE"])
def delete_alumno(id):
    try:
        eliminado = alumno_service.delete_alumno(id)
        if eliminado:
            return jsonify({"result": "Alumno eliminado correctamente"}), 200
        else:
            return jsonify({"error": "Error al eliminar el alumno"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
