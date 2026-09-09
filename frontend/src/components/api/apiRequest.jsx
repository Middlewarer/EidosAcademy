const API_URL = import.meta.env.VITE_API_URL ?? "";
let refreshFlight = null;
const SESSION_KEY = "auth_session";
export const getSessionId = () => localStorage.getItem(SESSION_KEY);
const sessionLock = (action) => {
    if (!globalThis.navigator?.locks) {
        throw new Error("Для обновления сессии нужен современный браузер и HTTPS (или localhost).");
    }
    return navigator.locks.request("eidos-auth-session", action);
};
const publicRoutes = new Set(["/api/token/", "/api/token/refresh/", "/api/register/", "/api/logout/"]);

export function clearSession() {
    localStorage.setItem(SESSION_KEY, crypto.randomUUID());
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.dispatchEvent(new Event("auth:expired"));
}

export function saveTokens(access, refresh) {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    localStorage.setItem(SESSION_KEY, crypto.randomUUID());
}

async function refreshAccess(failedAccess, version) {

    if (refreshFlight?.version === version) return refreshFlight.promise;
    const flight = { version };
    flight.promise = sessionLock(async () => {
        if (version !== getSessionId()) return null;
        const current = localStorage.getItem("access_token");
        if (current && current !== failedAccess) return current;
        const refresh = localStorage.getItem("refresh_token");
        if (!refresh) { clearSession(); return null; }
        const response = await fetch(`${API_URL}/api/token/refresh/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh }),
        });
        if (version !== getSessionId()) return null;
        if (!response.ok) {
            if (response.status === 401 || response.status === 400) {
                clearSession();
                return null;
            }
            throw new Error("Сервис авторизации временно недоступен.");
        }
        const data = await response.json();
        if (version !== getSessionId()) return null;
        if (!data.access) throw new Error("Некорректный ответ сервера авторизации.");
        localStorage.setItem("access_token", data.access);
        if (data.refresh) localStorage.setItem("refresh_token", data.refresh);
        return data.access;
    }).finally(() => { if (refreshFlight === flight) refreshFlight = null; });
    refreshFlight = flight;
    return flight.promise;
}

export async function apiRequest(url, options = {}) {
    const { auth = !publicRoutes.has(url), ...requestOptions } = options;
    const version = getSessionId();
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
    if (!auth || response.status !== 401 || version !== getSessionId()) return response;
    const current = localStorage.getItem("access_token");
    const token = current && current !== access ? current : await refreshAccess(access, version);
    if (!token || version !== getSessionId()) return response;
    const retry = await send(token);
    if (retry.status === 401 && version === getSessionId()
        && localStorage.getItem("access_token") === token) clearSession();
    return retry;
}

export async function logoutSession() {
    const version = getSessionId();
    return sessionLock(async () => {
        if (version !== getSessionId()) return;
        const refresh = localStorage.getItem("refresh_token");
        if (refresh) {
            const response = await apiRequest("/api/logout/", {
                method: "POST", auth: false, body: JSON.stringify({ refresh }),
            });
            if (!response.ok && response.status !== 401 && response.status !== 400) {
                throw new Error("Не удалось выйти. Попробуйте ещё раз.");
            }
        }
        if (version === getSessionId()) clearSession();
    });
}
