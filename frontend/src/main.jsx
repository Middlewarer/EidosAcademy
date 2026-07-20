import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import "./styles/reset.css"
import "./styles/global.css"
import "./styles/variables.css"
import Home from './pages/Home.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Home />
  </StrictMode>,
)
