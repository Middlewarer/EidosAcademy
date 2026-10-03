import { Link } from "react-router-dom";

const Footer = () => {
    return (
        <footer className="footer">


          <div className="container footer-content">


            <div className="logo">

              <span className="bulb">
                💡
              </span>

              Eidos<span>
                Academy
              </span>

            </div>


            <div className="footer-meta">
              <p>Создаем будущее через знания.</p>
              <nav className="footer-legal" aria-label="Юридическая информация">
                <Link to="/legal/privacy">Политика данных</Link>
                <Link to="/legal/terms">Соглашение</Link>
                <Link to="/legal/cookies">Cookie и хранилище</Link>
              </nav>
            </div>

            <Link className="footer-feedback-link" to="/feedback">Отзыв, идея или ошибка →</Link>


          </div>


        </footer>
    )
}

export default Footer;
