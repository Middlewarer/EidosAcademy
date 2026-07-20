import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import "./styles/reset.css"
import "./styles/global.css"
import "./styles/variables.css"
import Home from './pages/Home.jsx'
import Courses from "./pages/Courses.jsx"

createRoot(document.getElementById('root')).render(
    <Courses />
)
