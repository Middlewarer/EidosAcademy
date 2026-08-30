import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";



function Header() {
  const {user, loading} = useAuth();

  if (loading) {
    return <div>Загрузка до сих пор</div>
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
        {user? (<Link to="/profile" className="login-btn">
          {user?.username}
          </Link>) :
          (<Link to="/logout" className="login-btn">
          Выйти
        </Link>)
      }
        
        
      </div>
    </header>
    )
  }


export default Header