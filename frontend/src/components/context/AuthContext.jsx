import { createContext, useContext, useState, useEffect } from "react";
import { apiRequest } from "../api/apiRequest";
const AuthContext = createContext(null)

export function AuthProvider({children} ) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function checkAuth() {
            try {
                const response = await apiRequest("/api/me/")
                
                if (response.ok) {
                    const data = response.json();
                    setUser(data)
                }
                else {
                    localStorage.removeItem("refresh_token");
                    localStorage.removeItem("access_token");

                }
                
            }
            catch (error) {
                console.error("No", error)
            } finally {
                setLoading(false)
            }
        }

        checkAuth();
    }, [])


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