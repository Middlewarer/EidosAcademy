import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./layouts/Layout";
import Home from "./pages/Home";
import Courses from "./pages/Courses";
import CourseDetail from "./pages/CourseDetail";

const App = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<Layout />}>
                    <Route path="/" element={< Home/>} />
                    <Route path="/courses" element={< Courses/>} />
                    <Route path="/details" element={< CourseDetail/>} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App;