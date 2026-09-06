const API_URL = import.meta.env.VITE_API_URL;
let refreshFlight = null;
let sessionVersion = 0;
const publicRoutes = new Set(["/api/token/", "/api/token/refresh/", "/api/register/", "/api/logout/"]);

export function clearSession() {
    sessionVersion += 1;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.dispatchEvent(new Event("auth:expired"));
}

export function saveTokens(access, refresh) {
    sessionVersion += 1;
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
}

async function refreshAccess() {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) { clearSession(); return null; }
    const version = sessionVersion;
    if (refreshFlight?.version === version) return refreshFlight.promise;
    const flight = { version };
    flight.promise = (async () => {
        const response = await fetch(`${API_URL}/api/token/refresh/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh }),
        });
        if (version !== sessionVersion) return null;
        if (!response.ok) {
            if (response.status === 401 || response.status === 400) {
                clearSession();
                return null;
            }
            throw new Error("Сервис авторизации временно недоступен.");
        }
        const data = await response.json();
        if (version !== sessionVersion) return null;
        if (!data.access) throw new Error("Некорректный ответ сервера авторизации.");
        localStorage.setItem("access_token", data.access);
        if (data.refresh) localStorage.setItem("refresh_token", data.refresh);
        return data.access;
    })().finally(() => { if (refreshFlight === flight) refreshFlight = null; });
    refreshFlight = flight;
    return flight.promise;
}

export async function apiRequest(url, options = {}) {
    const { auth = !publicRoutes.has(url), ...requestOptions } = options;
    const version = sessionVersion;
    const access = localStorage.getItem("access_token");
    const send = (token) => {
        const headers = new Headers(requestOptions.headers);
        if (!(requestOptions.body instanceof FormData) && !headers.has("Content-Type")) {
            headers.set("Content-Type", "application/json");
        }
        if (auth && token) headers.set("Authorization", `Bearer ${token}`);
        return fetch(`${API_URL}${url}`, { ...requestOptions, headers });
    };
    const response = await send(access);
    if (!auth || response.status !== 401 || version !== sessionVersion) return response;
    const current = localStorage.getItem("access_token");
    const token = current && current !== access ? current : await refreshAccess();
    if (!token || version !== sessionVersion) return response;
    const retry = await send(token);
    if (retry.status === 401 && version === sessionVersion) clearSession();
    return retry;
}

export async function logoutSession() {
    // Wait for rotation so that logout revokes the latest refresh token.
    if (refreshFlight) await refreshFlight.promise;
    const refresh = localStorage.getItem("refresh_token");
    if (refresh) {
        const response = await apiRequest("/api/logout/", {
            method: "POST", auth: false, body: JSON.stringify({ refresh }),
        });
        if (!response.ok && response.status !== 401 && response.status !== 400) {
            throw new Error("Не удалось выйти. Попробуйте ещё раз.");
        }
    }
    clearSession();
}
