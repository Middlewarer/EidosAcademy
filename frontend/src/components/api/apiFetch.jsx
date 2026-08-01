export async function apiFetch(url, options = {}) {

    const token = localStorage.getItem("access");

    const headers = {
        ...options.headers,
        Authorization: `Bearer ${token}`,
    };

    return fetch(url, {
        ...options,
        headers,
    });
}