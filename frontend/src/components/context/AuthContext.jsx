import { createContext, useContext, useState, useEffect } from "react";
import { apiRequest, saveTokens, logoutSession } from "../api/apiRequest";
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        let active = true;
        const expired = () => setUser(null);
        const storageChanged = (event) => {
            if (event.key === null || event.key === "access_token") expired();
        };
        window.addEventListener("auth:expired", expired);
        window.addEventListener("storage", storageChanged);
        async function checkAuth() {
            try {
                if (!localStorage.getItem("access_token") && !localStorage.getItem("refresh_token")) return;
                const response = await apiRequest("/api/me/");
                if (response.ok) {
                    const data = await response.json();
                    if (active && localStorage.getItem("access_token")) setUser(data);
                }
            } catch (error) { console.error("Не удалось проверить авторизацию:", error); }
            finally { if (active) setLoading(false); }
        }
        checkAuth();
        return () => {
            active = false;
            window.removeEventListener("auth:expired", expired);
            window.removeEventListener("storage", storageChanged);
        };
    }, []);
    function login(access, refresh, userData) {
        saveTokens(access, refresh);
        setUser(userData);
    }
    async function logout() { await logoutSession(); setUser(null); }
    return <AuthContext.Provider value={{ user, setUser, loading, login, logout }}>{children}</AuthContext.Provider>;
}
// The existing public hook is kept here to preserve component imports.
// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() { return useContext(AuthContext); }
