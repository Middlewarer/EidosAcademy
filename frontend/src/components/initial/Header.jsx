import { Link } from "react-router-dom";

function Header() {
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
        <Link to="/login" className="login-btn">
          Войти
        </Link>
        
      </div>
    </header>
    )
}

export default Header