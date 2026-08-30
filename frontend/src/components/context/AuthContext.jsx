import { createContext, useContext, useState, useEffect } from "react";
import { apiRequest } from "../api/apiRequest";
const AuthContext = createContext(null)

export function AuthProvider({children} ) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
    async function checkAuth() {
        const accessToken = localStorage.getItem("access_token");
        const refreshToken = localStorage.getItem("refresh_token");
        
        // Если нет токенов — выходим
        if (!accessToken || !refreshToken) {
            setLoading(false);
            return;
        }

        try {
            // Пробуем получить профиль
            let response = await apiRequest("/api/me/");
            
            if (response.ok) {
                const data = await response.json();
                setUser(data);
                setLoading(false);
                return;
            }

            // ✅ Если токен протух (401) — пробуем обновить
            if (response.status === 401) {
                const refreshResponse = await fetch("http://127.0.0.1:8000/api/token/refresh/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ refresh: refreshToken })
                });

                if (refreshResponse.ok) {
                    const refreshData = await refreshResponse.json();
                    
                    // ✅ Сохраняем новый access_token
                    localStorage.setItem("access_token", refreshData.access);
                    
                    // ✅ Повторяем запрос профиля с новым токеном
                    response = await apiRequest("/api/me/");
                    if (response.ok) {
                        const data = await response.json();
                        setUser(data);
                    }
                } else {
                    // ❌ Refresh токен тоже протух — разлогиниваем
                    localStorage.removeItem("access_token");
                    localStorage.removeItem("refresh_token");
                }
            }
        }
        catch (error) {
            console.error("Ошибка проверки авторизации:", error);
        } finally {
            setLoading(false);
        }
    }

    checkAuth();
}, []);


function login(access, refresh, userData) {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    setUser(userData);
}


function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
}

return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );

}

export function useAuth() {
    return useContext(AuthContext)
}