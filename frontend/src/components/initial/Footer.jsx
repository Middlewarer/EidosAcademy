import { Link } from "react-router-dom";
import "../../styles/Legal.css";

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

            </div>

            <Link className="footer-feedback-link" to="/feedback">Отзыв, идея или ошибка →</Link>


          </div>


        </footer>
    )
}

export default Footer;
