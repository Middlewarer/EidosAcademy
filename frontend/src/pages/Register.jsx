import { apiRequest } from "../components/api/apiRequest";
import { Link, useLocation } from "react-router-dom";
import "../styles/Login.css";
import {toast} from "react-hot-toast";
import  {useNavigate}  from "react-router-dom";
import { useState } from "react";

function Register() {
  const location = useLocation();
  const navigator = useNavigate();
  const [personalDataConsent, setPersonalDataConsent] = useState(false);
  const [termsAccepted, setTermsAccepted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const handleSubmit = async (e) => {
    e.preventDefault();
    const username = e.target.elements.username.value;
    const password = e.target.elements.password.value;
    const password2 = e.target.elements.password2.value;
    


    if (password !== password2) {
      toast.error("Пароли не совпадают.");
      return;
    }
    if (submitting) return;
    setSubmitting(true);

    try {
        const response = await apiRequest("/api/register/", {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({"username": username,
            "password": password,
            "password2": password2,
            "personal_data_consent": personalDataConsent,
            "terms_accepted": termsAccepted
          })
        })

        if (!response.ok) {
          const data = await response.json();
          toast.error(Object.values(data.error ?? data).flat().join(" ") || "Ошибка регистрации.");
          return;
        }


      toast.success("Регистрация прошла успешно");
      navigator('/login', { state: location.state });
    } catch {
      toast.error("Не удалось связаться с сервером.");
    } finally {
      setSubmitting(false);
    }
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
              <span>Имя пользователя</span>
              <input
                type="text"
                name="username"
                placeholder="Как к вам обращаться?"
                autoComplete="username"
                required
                autoFocus
                maxLength={150}
              />
            </label>

            <label className="login-field">
              <span>Пароль</span>
              <input
                type="password"
                name="password"
                placeholder="Придумайте пароль"
                autoComplete="new-password"
                required
                minLength={8}
              />
            </label>

            <label className="login-field">
              <span>Повторите пароль</span>
              <input
                type="password"
                name="password2"
                placeholder="Повторите пароль"
                autoComplete="new-password"
                required
              />
            </label>

            <p className="login-password-hint">Минимум 8 символов. Не используйте распространённый пароль или только цифры.</p>

            <div className="login-legal-group">
              <label className="legal-checkbox">
                <input type="checkbox" required checked={personalDataConsent} onChange={(event) => setPersonalDataConsent(event.target.checked)} />
                <span>Даю отдельное <Link to="/legal/consent" target="_blank" rel="noreferrer">согласие на обработку персональных данных</Link>.</span>
              </label>

              <label className="legal-checkbox">
                <input type="checkbox" required checked={termsAccepted} onChange={(event) => setTermsAccepted(event.target.checked)} />
                <span>Принимаю <Link to="/legal/terms" target="_blank" rel="noreferrer">пользовательское соглашение</Link>.</span>
              </label>
            </div>

            <button type="submit" className="login-submit" disabled={submitting}>
              {submitting ? "Создаём аккаунт…" : "Создать аккаунт"}
            </button>
          </form>

          <p className="login-footer-text">
            Уже есть аккаунт?{" "}
            <Link to="/login" state={location.state} className="login-link">
              Войти
            </Link>
          </p>
        </div>
      </section>
    </main>
  );
}
export default Register;
