import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import "./styles/reset.css"
import "./styles/global.css"
import "./styles/variables.css"
import { AuthProvider } from './components/context/AuthContext.jsx'
import App from './App.jsx'
import { FavoritesProvider } from './components/context/FavoritesContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
    <FavoritesProvider><App /></FavoritesProvider>
  </AuthProvider>
  </StrictMode>,
)
