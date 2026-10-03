import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { apiRequest, saveTokens } from "../components/api/apiRequest";
import { useAuth } from "../components/context/AuthContext";
import "../styles/Login.css";

function Login() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, login } = useAuth();
  const destination = location.state?.from;
  const returnTo = typeof destination === "string"
    && destination.startsWith("/")
    && !destination.startsWith("//")
    && !destination.startsWith("/login")
    && !destination.startsWith("/register")
    ? destination
    : "/courses";
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    if (submitting) return;
    setSubmitting(true);

    try {
      const response = await apiRequest("/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username.trim(), password }),
      });
      const data = await response.json();

      if (!response.ok || !data.access || !data.refresh) {
        toast.error(response.status === 429
          ? "Слишком много попыток. Попробуйте позже."
          : "Не удалось войти. Проверьте логин и пароль.");
        return;
      }

      saveTokens(data.access, data.refresh);
      const meResponse = await apiRequest("/api/me/");
      if (!meResponse.ok) {
        toast.error("Не удалось загрузить профиль.");
        return;
      }

      const userData = await meResponse.json();
      login(data.access, data.refresh, userData);
      toast.success("Вход выполнен!");
      navigate(returnTo, { replace: true });
    } catch {
      toast.error("Не удалось связаться с сервером. Попробуйте ещё раз.");
    } finally {
      setSubmitting(false);
    }
  }

  useEffect(() => {
    if (user) navigate(returnTo, { replace: true });
  }, [user, navigate, returnTo]);

  return (
    <main className="login-page">
      <section className="login-main" aria-labelledby="login-title">
        <div className="login-card">
          <header className="login-card-header">
            <Link to="/" className="login-logo" aria-label="Eidos Academy — главная">
              <span className="login-logo-icon" aria-hidden="true">💡</span>
              Eidos<span>Academy</span>
            </Link>
            <h1 id="login-title">Вход</h1>
            <p>Продолжите обучение с того места, где остановились.</p>
          </header>

          <form className="login-form" onSubmit={handleSubmit}>
            <label className="login-field">
              <span>Логин</span>
              <input type="text" name="username" placeholder="Введите логин" autoComplete="username" required autoFocus maxLength={150} value={username} onChange={(event) => setUsername(event.target.value)} />
            </label>
            <label className="login-field">
              <span>Пароль</span>
              <input type="password" name="password" placeholder="Введите пароль" autoComplete="current-password" required value={password} onChange={(event) => setPassword(event.target.value)} />
            </label>
            <button type="submit" className="login-submit" disabled={submitting}>
              {submitting ? "Входим…" : "Войти"}
            </button>
          </form>

          <p className="login-footer-text">
            Нет аккаунта?{" "}
            <Link to="/register" state={{ from: returnTo }} className="login-link">Зарегистрироваться</Link>
          </p>
        </div>
      </section>
    </main>
  );
}

export default Login;
