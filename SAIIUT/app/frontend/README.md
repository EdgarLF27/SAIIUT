# Guion explicativo del frontend de SAIIUT

## Estructura general

- El frontend está compuesto por archivos HTML individuales para cada módulo administrativo: usuarios, materias, calificaciones, configuración, etc.
- Cada archivo HTML representa una vista o sección específica del sistema.

## Diseño y estilos

- Se utiliza **TailwindCSS** para la maquetación y estilos utilitarios, logrando un diseño moderno y responsivo.
- Se emplean fuentes personalizadas (IBM Plex Sans) y **Font Awesome** para iconografía.
- El layout es consistente: sidebar lateral, encabezado superior, contenido principal y footer informativo.

## Componentes y funcionalidad

- **Sidebar:** Navegación lateral fija con enlaces a los distintos módulos.
- **Tabs:** En los formularios de usuarios, se usan tabs para alternar entre registro de alumnos, docentes y administradores.
- **Formularios:** Cada entidad (alumno, docente, admin, materia) tiene su propio formulario de registro y edición, con validaciones visuales y feedback inmediato.
- **Tablas:** Listados de registros con filtros y acciones (editar, eliminar) para facilitar la gestión.
- **Modales:** Los formularios de edición y registro extra se muestran en modales tipo overlay, con fondo desenfocado y controles accesibles.

## Interactividad

- Se usa **JavaScript vanilla** embebido en los archivos HTML para:
  - Cambiar de tabs y mostrar/ocultar formularios.
  - Abrir/cerrar modales.
  - Validar campos en tiempo real (colores de borde según validez).
  - Realizar peticiones `fetch` al backend para operaciones CRUD.
  - Actualizar dinámicamente tablas y formularios tras operaciones.

## Buenas prácticas

- El código mantiene una estructura clara y reutiliza estilos y componentes visuales.
- Los formularios y tablas son responsivos y accesibles.
- Se separan claramente las vistas y funcionalidades por archivo.

## Sugerencias

- Centralizar scripts y estilos comunes para facilitar el mantenimiento.
- Considerar migrar a un framework si el proyecto crece (React, Vue, etc.).
- Mantener la consistencia visual y de experiencia de usuario en todos los módulos.

---
Este guion resume cómo está construido y organizado el frontend del sistema SAIIUT.
