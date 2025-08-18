# Guion explicativo del backend de SAIIUT

## Estructura general

- El backend está organizado en una carpeta separada (`backend`) dentro del proyecto.
- Incluye archivos y módulos para manejar la lógica de negocio, rutas, controladores y conexión a la base de datos.

## Tecnologías y arquitectura

- El backend utiliza **Python** con el framework **Flask** para crear una API RESTful.
- Se emplea una arquitectura modular: cada entidad principal (alumnos, docentes, admins, materias, calificaciones) tiene su propio archivo de rutas y lógica.
- La comunicación con el frontend se realiza mediante endpoints HTTP que reciben y responden en formato JSON.

## Componentes principales

- **Rutas (Endpoints):**  
  - CRUD para alumnos, docentes, administradores y materias.
  - Endpoints para operaciones específicas como filtros, búsquedas y autenticación.
- **Controladores:**  
  - Funciones que procesan la lógica de cada endpoint, validan datos y gestionan respuestas.
- **Modelos y conexión a base de datos:**  
  - Uso de un ORM (como SQLAlchemy) o consultas SQL directas para interactuar con la base de datos.
  - Modelos que representan las tablas principales del sistema.
- **Validaciones y seguridad:**  
  - Validación de datos de entrada en cada endpoint.
  - Gestión básica de autenticación y control de acceso según roles.

## Interacción con el frontend

- El backend expone endpoints que el frontend consume mediante `fetch` o AJAX.
- Todas las operaciones de registro, edición, consulta y eliminación se realizan a través de la API.
- Las respuestas son en formato JSON, facilitando la integración con el frontend.

## Buenas prácticas

- Separación clara de responsabilidades: rutas, lógica de negocio y acceso a datos.
- Uso de respuestas estructuradas y manejo de errores.
- Código comentado y organizado por módulos.

## Sugerencias

- Centralizar la configuración y variables sensibles (por ejemplo, en un archivo `.env`).
- Implementar autenticación robusta y control de permisos si el sistema crece.
- Documentar los endpoints con herramientas como Swagger o Postman.
- Considerar el uso de Blueprints de Flask para mayor escalabilidad.

---
Este guion resume cómo está construido y organizado el backend del sistema SAIIUT.
