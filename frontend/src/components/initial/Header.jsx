import { useEffect, useState } from "react";
import { Link, NavLink, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Header() {
  const { user, loading, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname, location.hash]);

  const handleLogout = (e) => {
    e.preventDefault();
    logout();
    navigate("/login");
  };

  return (
    <header className="header">
      <div className="container nav">
        <Link to="/" className="logo" aria-label="EidosAcademy — главная">
          <span className="bulb">💡</span>
          Eidos<span>Academy</span>
        </Link>

        <button
          type="button"
          className={`nav-toggle ${menuOpen ? "is-open" : ""}`}
          aria-label={menuOpen ? "Закрыть меню" : "Открыть меню"}
          aria-expanded={menuOpen}
          aria-controls="main-navigation"
          onClick={() => setMenuOpen((value) => !value)}
        >
          <span />
          <span />
        </button>

        <div className={`nav-panel ${menuOpen ? "is-open" : ""}`}>
          <nav id="main-navigation" aria-label="Основная навигация">
            <NavLink to="/" end>Главная</NavLink>
            <NavLink to="/courses">Курсы</NavLink>
          <a href="/#learning">Обучение</a>
          <a href="/#reviews">Отзывы</a>
          </nav>

          <div className="header-actions">
            {loading ? (
              <span className="header-actions-loading" aria-label="Проверяем авторизацию" />
            ) : user ? (
              <>
                <Link to="/profile" className="profile-btn">
                  <span className="profile-btn-avatar" aria-hidden="true">
                    {(user.first_name || user.username || "П").charAt(0).toUpperCase()}
                  </span>
                  Профиль
                </Link>
                <button type="button" className="logout-btn" onClick={handleLogout}>
                  Выйти
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="login-link-btn">Войти</Link>
                <Link to="/register" className="register-btn">Регистрация</Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
