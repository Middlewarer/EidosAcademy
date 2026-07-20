import Button from "../Button"

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


          <Button type='button'>Войти</Button>

        </div>
      </header> 
    )
}

export default Header