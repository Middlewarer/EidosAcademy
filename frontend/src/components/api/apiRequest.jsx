export async function apiRequest(url, options = {}) {
    const accessToken = localStorage.getItem("access_token")

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`
    }

    const response = await fetch(`http://127.0.0.1:8000${url}`, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        console.warn("Credentials were wrong")
    }

    return response
}