import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./layouts/Layout";
import Home from "./pages/Home";
import Courses from "./pages/Courses";
import CourseDetail from "./pages/CourseDetail";
import ModulePage from "./pages/ModulePage"
import Login from "./pages/Login"
import ProfilePage from "./pages/ProfilePage";
import Toaster from 'react-hot-toast';

const App = () => {
    return (
        
        <BrowserRouter>
        <Toaster />
            <Routes>
                <Route element={<Layout />}>
                    <Route path="/" element={< Home/>} />
                    <Route path="/courses" element={<Courses />} />
                    <Route path="/courses/:courseId" element={<CourseDetail />} />
                    <Route path="/courses/:courseId/modules/:moduleId" element={< ModulePage/>}/>
                    <Route path="/login" element={< Login/>}/>
                    <Route path="/profile" element={< ProfilePage/>}/>
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App;
