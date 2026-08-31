import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./layouts/Layout";
import Home from "./pages/Home";
import Courses from "./pages/Courses";
import CourseDetail from "./pages/CourseDetail";
import ModulePage from "./pages/ModulePage";
import Login from "./pages/Login";
import ProfilePage from "./pages/ProfilePage";
import { Toaster } from 'react-hot-toast'; // ✅ Правильный импорт
import ProtectedRoute from "./components/ProtectedRoute";

const App = () => {
    return (
        <BrowserRouter>
            <Toaster />
            <Routes>
                {/* Страница входа без Layout */}
                <Route path="/login" element={<Login />} />
                
                {/* Все страницы с Layout */}
                <Route element={<Layout />}>
                    {/* Публичные маршруты */}
                    <Route path="/" element={<Home />} />
                    <Route path="/courses" element={<Courses />} />
                    
                    {/* Защищенные маршруты */}
                    <Route element={<ProtectedRoute />}>
                        <Route path="/courses/:courseId" element={<CourseDetail />} />
                        <Route path="/courses/:courseId/modules/:moduleId" element={<ModulePage />} />
                        <Route path="/profile" element={<ProfilePage />} />
                    </Route>
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;