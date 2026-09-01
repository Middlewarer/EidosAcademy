import { Link } from "react-router-dom";
import "../styles/Login.css";
import {toast} from "react-hot-toast";
import  {useNavigate}  from "react-router-dom";

function Register() {
  const navigator = useNavigate();
  const handleSubmit = (e) => {
    e.preventDefault();
    const username = e.target.elements.username.value;
    const password = e.target.elements.password.value;
    const password2 = e.target.elements.password2.value;
    

    const registerUser = async () => {
        
        const response = await fetch("http://127.0.0.1:8000/api/register/", {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({"username": username,
            "password": password,
            "password2": password2
          })
        })

        if (!response.ok || password != password2) {
          toast.error("Ошибка в создании пользователя")
          return;
        }


      toast.success("Регистрация прошла успешно")
      navigator('/login');  
    }

    registerUser();
    
    return;

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

          <form className="login-form" onSubmit={handleSubmit}>
            <label className="login-field">
              <span>username</span>
              <input
                type="text"
                name="username"
                placeholder="Как к вам обращаться?"
                autoComplete="name"
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
                name="password2"
                placeholder="Повторите пароль"
                autoComplete="new-password"
              />
            </label>

            <button type="submit" className="login-submit">
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
