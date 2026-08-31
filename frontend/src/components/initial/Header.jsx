import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Button from "../Button";
import { useNavigate } from "react-router-dom";

function Header() {
  const { user, loading, logout } = useAuth();
  const navigator = useNavigate();

  const handleLogout = (e) => {
    e.preventDefault();
    logout();
    navigator("login/")
  };

  if (loading) {
    return <div>Загрузка до сих пор</div>;
  }

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
        
        {user ? (
          // Если пользователь авторизован - показываем кнопку "Выйти"
          <Button className="login-btn" onClick={handleLogout}>
            Выйти
          </Button>
        ) : (
          // Если не авторизован - показываем "Войти"
          <Link to="login/" className="login-btn">
            Войти
          </Link>
        )}
      </div>
    </header>
  );
}

export default Header;