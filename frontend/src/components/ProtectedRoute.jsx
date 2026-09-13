import { useAuth } from "./context/AuthContext"
import { Navigate, Outlet, useLocation } from "react-router-dom";

const ProtectedRoute = () => {
    const location = useLocation();
    const {user, loading} = useAuth();

    if (loading) {
        return <div>Проверяем вход…</div>
    }

    if (!user) {
        return <Navigate to="/login" state={{ from: location.pathname + location.search }} replace />
    }

    return <Outlet/>
}

export default ProtectedRoute;