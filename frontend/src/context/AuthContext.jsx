import { createContext, useState } from "react";


export const AuthContext = createContext();


export const AuthProvider = ({children}) => {

    const [isAuthenticated, setIsAuthenticated] = useState(
        Boolean(localStorage.getItem("access"))
    );


    const login = (access, refresh) => {

        localStorage.setItem(
            "access",
            access
        );

        localStorage.setItem(
            "refresh",
            refresh
        );

        setIsAuthenticated(true);
    };


    const logout = () => {

        localStorage.removeItem("access");
        localStorage.removeItem("refresh");

        setIsAuthenticated(false);
    };


    return (
        <AuthContext.Provider
            value={{
                isAuthenticated,
                login,
                logout
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};