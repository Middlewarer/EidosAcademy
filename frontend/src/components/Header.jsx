function Header() {
    return (
       <header className="header">
        <div className="container nav">

          <div className="logo">
            <span className="bulb">💡</span>
            Eidos<span>Academy</span>
          </div>


          <nav>
            <a href="#courses">Курсы</a>
            <a href="#about">О нас</a>
            <a href="#learning">Обучение</a>
            <a href="#reviews">Отзывы</a>
          </nav>


          <button className="login-btn">
            Войти
          </button>

        </div>
      </header> 
    )
}

export default Header