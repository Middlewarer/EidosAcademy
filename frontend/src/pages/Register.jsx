import { Link } from "react-router-dom";
import "../styles/Login.css";

function Register() {
  const handleSubmit = async (e) => {
    e.preventDefault()
  }
  return (
    <main className="login-page">
      <section className="login-main">
        <div className="login-card">
          <header className="login-card-header">
            <Link to="/" className="login-logo" aria-label="Eidos Academy — главная">
              <span className="login-logo-icon" aria-hidden="true">💡</span>
              Eidos<span>Academy</span>
            </Link>

            <h1>Создайте аккаунт</h1>
            <p>Начните учиться в своём темпе уже сегодня.</p>
          </header>

          <form className="login-form">
            <label className="login-field">
              <span>Имя</span>
              <input
                type="text"
                name="name"
                placeholder="Как к вам обращаться?"
                autoComplete="name"
              />
            </label>

            <label className="login-field">
              <span>Электронная почта</span>
              <input
                type="email"
                name="email"
                placeholder="you@example.com"
                autoComplete="email"
              />
            </label>

            <label className="login-field">
              <span>Пароль</span>
              <input
                type="password"
                name="password"
                placeholder="Придумайте пароль"
                autoComplete="new-password"
              />
            </label>

            <label className="login-field">
              <span>Повторите пароль</span>
              <input
                type="password"
                name="passwordConfirmation"
                placeholder="Повторите пароль"
                autoComplete="new-password"
              />
            </label>

            <label className="login-checkbox">
              <input type="checkbox" name="terms" />
              <span>
                Я принимаю <a href="#terms" className="login-link">условия использования</a>
              </span>
            </label>

            <button type="button" className="login-submit">
              Создать аккаунт
            </button>
          </form>

          <p className="login-footer-text">
            Уже есть аккаунт?{" "}
            <Link to="/login" className="login-link">
              Войти
            </Link>
          </p>
        </div>
      </section>
    </main>
  );
}

export default Register;
