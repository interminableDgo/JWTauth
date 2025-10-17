function getApiUrl() {
    try {
        const cfg = JSON.parse(localStorage.getItem('config'));
        if (cfg && cfg.ip && cfg.port) return `http://${cfg.ip}:${cfg.port}`;
    } catch (e) {
        // ignore
    }
    return 'http://localhost:5000';
}

let apiUrl = getApiUrl();

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${apiUrl}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            logMessage('Login exitoso');
            console.info('Login response', data);
            showTokens();
        } else {
            logMessage(data.message);
        }
    } catch (error) {
        logMessage('Error al iniciar sesión');
    }
});

document.getElementById('register-btn').addEventListener('click', async () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${apiUrl}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        logMessage(data.message);
    } catch (error) {
        logMessage('Error al registrar usuario');
    }
});

document.getElementById('refresh-btn').addEventListener('click', async () => {
    const refreshToken = localStorage.getItem('refresh_token');

    try {
        const response = await fetch(`${apiUrl}/auth/refresh`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${refreshToken}`
            }
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('access_token', data.access_token);
            logMessage('Token refrescado exitosamente');
        } else {
            logMessage(data.message);
        }
    } catch (error) {
        logMessage('Error al refrescar token');
    }
});

document.getElementById('profile-btn').addEventListener('click', async () => {
    const accessToken = localStorage.getItem('access_token');

    try {
        const response = await fetch(`${apiUrl}/api/profile`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });

        const data = await response.json();
        logMessage(JSON.stringify(data));
    } catch (error) {
        logMessage('Error al acceder al perfil');
    }
});

document.getElementById('save-config-btn').addEventListener('click', () => {
    const ip = prompt('Ingrese la IP del microservicio:');
    const port = prompt('Ingrese el puerto del microservicio:');
    const endpoints = ['/auth/register', '/auth/login', '/auth/refresh', '/api/profile'];

    localStorage.setItem('config', JSON.stringify({ ip, port, endpoints }));
    // update apiUrl in memory so the app uses the new config immediately
    apiUrl = getApiUrl();
    logMessage('Configuración guardada en localStorage');
    logMessage(`API actual: ${apiUrl}`);
});

function logMessage(message) {
    const logsDiv = document.getElementById('logs');
    const logEntry = document.createElement('div');
    logEntry.textContent = message;
    logsDiv.appendChild(logEntry);
}

function showTokens() {
    const at = localStorage.getItem('access_token') || '';
    const rt = localStorage.getItem('refresh_token') || '';
    const tokensDiv = document.getElementById('tokens');
    if (tokensDiv) tokensDiv.textContent = `Access: ${at}\nRefresh: ${rt}`;
}

// show tokens on load if present
document.addEventListener('DOMContentLoaded', () => {
    apiUrl = getApiUrl();
    showTokens();
});