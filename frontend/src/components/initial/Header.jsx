import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";



function Header() {
  const {user} = useAuth();
  return (
       <header className="header">
      <div className="container nav">
        <Link to="/" className="logo">
          <span className="bulb">💡</span>
          Eidos<span>Academy</span>
        </Link>
        <nav>
          <Link to="/courses">Курсы</Link>
          <a href="/#about">О нас</a>
          <a href="/#learning">Обучение</a>
          <a href="/#reviews">Отзывы</a>
        </nav>
        {user? (<Link to="/profile" className="login-btn">
          {user?.username} <Link to="/logout" className="login-btn">
          Выйти
        </Link>
        </Link>) : ((<Link to="/login" className="login-btn">
          Войти
        </Link>))}
        
        
      </div>
    </header>
    )
}

export default Header