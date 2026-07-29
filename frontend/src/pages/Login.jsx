import { Link } from "react-router-dom";
import "../styles/Login.css";
import { useState } from "react";
import { useEffect } from "react";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";


function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const {login} = useContext(AuthContext)

  const navigate = useNavigate();

  

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("http://127.0.0.1:8000/api/token/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        username,
        password
      })
    })

    const data = await response.json();

    localStorage.setItem("access", data.access)
    localStorage.setItem("refresh", data.refresh)

    login(
    data.access,
    data.refresh
    );

    navigate("/")
  }
  useEffect(
  () => {

  }, []
)
  return (
    <div className="login-page">
      <main className="login-main">
        <section className="login-card">
          <div className="login-card-header">
            <Link to="/" className="login-logo">
              <span className="login-logo-icon">💡</span>
              Eidos<span>Academy</span>
            </Link>
            <h1>Вход в аккаунт</h1>
            <p>Продолжите обучение с того места, где остановились.</p>
          </div>

          <form className="login-form" onSubmit={handleSubmit}>
            <label className="login-field">
              <span>username</span>
              <input
                type="text"
                name="username"
                placeholder="you@example.com"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </label>

            <label className="login-field">
              <span>Пароль</span>
              <input
                type="password"
                name="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </label>

            <div className="login-form-row">
              <label className="login-checkbox">
                <input type="checkbox" name="remember" />
                <span>Запомнить меня</span>
              </label>

            </div>

            <button type="submit" className="login-submit">
              Войти
            </button>
          </form>

          <p className="login-footer-text">
            Нет аккаунта?{" "}
            <Link to="/register" className="login-link">
              Зарегистрироваться
            </Link>
          </p>
        </section>
      </main>
    </div>
  );
}

export default Login;
