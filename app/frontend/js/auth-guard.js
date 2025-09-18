document.addEventListener('DOMContentLoaded', async () => {
    const API_BASE_URL = 'http://localhost:5000';
    const path = window.location.pathname;
    let expectedRole = null;

    if (path.includes('/Admin/')) {
        expectedRole = 'admin';
    } else if (path.includes('/Docente/')) {
        expectedRole = 'profesor';
    } else if (path.includes('/Alumno/')) {
        expectedRole = 'alumno';
    }

    // Si es una página que no requiere rol (como el login), no hacemos nada.
    if (!expectedRole) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/me`, { credentials: 'include' });

        if (!response.ok) {
            // Si no está autorizado, siempre al login.
            if (response.status === 401) {
                console.log('AuthGuard: No autorizado. Redirigiendo a login.');
                window.location.href = '../login.html';
                return;
            }
            throw new Error('Error del servidor al verificar la sesión.');
        }

        const data = await response.json();
        const userRole = data.role;

        // Guardar datos en sessionStorage para que otras páginas los usen
        sessionStorage.setItem('userData', JSON.stringify(data.profile));
        sessionStorage.setItem('userRole', userRole);

        if (userRole !== expectedRole) {
            console.log(`AuthGuard: Rol incorrecto. Esperado: ${expectedRole}, Obtenido: ${userRole}. Redirigiendo.`);
            // Redirigir al índice correspondiente a su rol
            switch (userRole) {
                case 'admin':
                    window.location.href = '../Admin/IndexAdmin.html';
                    break;
                case 'profesor':
                    window.location.href = '../Docente/IndexDocente.html';
                    break;
                case 'alumno':
                    window.location.href = '../Alumno/index.html';
                    break;
                default:
                    // Si tiene un rol desconocido, al login
                    window.location.href = '../login.html';
            }
        }
        // Si el rol es correcto, el usuario puede quedarse en la página.

    } catch (error) {
        console.error('AuthGuard Error:', error);
        // Ante cualquier error, es más seguro redirigir al login.
        window.location.href = '../login.html';
    }
});
