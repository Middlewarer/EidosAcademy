import { Link } from "react-router-dom";
import "../styles/ProfileSettings.css";
import { apiRequest } from "../components/api/apiRequest";
import { useAuth } from "../components/context/AuthContext";
import { useState } from "react";
import toast from "react-hot-toast";

export default function ProfileSettings() {

  const [firstName, setFirstName] = useState(null);
  const [lastName, setLastName] = useState(null);
  const [email, setEmail] = useState(null);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const { user, setUser } = useAuth();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await apiRequest("/api/me/", {
        method: "PATCH",
        body: JSON.stringify({
          first_name: firstName ?? user?.first_name ?? "",
          last_name: lastName ?? user?.last_name ?? "",
          email: email ?? user?.email ?? "",
        }),
      });
      const data = await response.json();

      if (!response.ok) {
        toast.error(Object.values(data).flat().join(" ") || "Не удалось сохранить изменения.");
        return;
      }

      setUser(data);
      toast.success("Данные профиля сохранены.");
    } catch {
      toast.error("Не удалось связаться с сервером. Попробуйте ещё раз.");
    }
  };

  const handlePasswordSubmit = async (event) => {
    event.preventDefault();
    if (newPassword !== confirmPassword) {
      toast.error("Пароли не совпадают.");
      return;
    }

    try {
      const response = await apiRequest("/api/me/password/", {
        method: "POST",
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
          confirm_password: confirmPassword,
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        toast.error(Object.values(data).flat().join(" ") || "Не удалось обновить пароль.");
        return;
      }
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      toast.success("Пароль обновлён.");
    } catch {
      toast.error("Не удалось связаться с сервером. Попробуйте ещё раз.");
    }
  };

  return (
    <main className="profile-settings">
      <div className="settings-container">
        <Link to="/profile" className="settings-back">← Назад в профиль</Link>

        <header className="settings-heading">
          <span className="settings-eyebrow">Личный кабинет</span>
          <h1>Редактирование профиля</h1>
          <p>Ваша информация и безопасность аккаунта — в одном месте.</p>
        </header>

        <div className="settings-layout">
          <aside className="settings-aside">
            <div className="settings-avatar" aria-hidden="true">
              <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="12" cy="8" r="4" />
                <path d="M4 21v-2a8 8 0 0 1 16 0v2" />
              </svg>
            </div>
            <h2>Ваш профиль</h2>
            <p>Добавьте имя, чтобы сделать обучение чуть более личным.</p>
            <nav className="settings-nav" aria-label="Разделы настроек">
              <a href="#personal-details">Личные данные <span aria-hidden="true">↗</span></a>
              <a href="#account-password">Безопасность <span aria-hidden="true">↗</span></a>
            </nav>
          </aside>

          <div className="settings-sections">
            <section className="settings-card" id="personal-details" aria-labelledby="personal-title">
              <div className="settings-card-heading">
                <span className="settings-step" aria-hidden="true">01</span>
                <div>
                  <h2 id="personal-title">Личные данные</h2>
                  <p>Как к вам обращаться и куда отправлять письма.</p>
                </div>
              </div>

              <form className="settings-form" onSubmit={handleSubmit}>
                <div className="settings-field-grid">
                  <div className="settings-field">
                    <label htmlFor="first-name">Имя</label>
                    <input id="first-name" name="first_name" type="text" autoComplete="given-name" placeholder="Ваше имя" value={firstName ?? user?.first_name ?? ""} onChange={(e) => {setFirstName(e.target.value)}}/>
                  </div>
                  <div className="settings-field">
                    <label htmlFor="last-name">Фамилия</label>
                    <input id="last-name" name="last_name" type="text" autoComplete="family-name" placeholder="Ваша фамилия" value={lastName ?? user?.last_name ?? ""} onChange={(e) => {setLastName(e.target.value)}}/>
                  </div>
                </div>
                <div className="settings-field">
                  <label htmlFor="profile-email">Электронная почта</label>
                  <input id="profile-email" name="email" type="email" autoComplete="email" placeholder="you@example.com" aria-describedby="email-hint" value={email ?? user?.email ?? ""} onChange={(e) => {setEmail(e.target.value)}}/>
                  <p id="email-hint" className="settings-hint">Ваша контактная почта. Для входа используется логин.</p>
                </div>
                <div className="settings-actions">
                  <Link to="/profile" className="settings-cancel">Отмена</Link>
                  <button type="submit" className="settings-primary">Сохранить изменения</button>
                </div>
              </form>
            </section>

            <section className="settings-card" id="account-password" aria-labelledby="password-title">
              <div className="settings-card-heading">
                <span className="settings-step" aria-hidden="true">02</span>
                <div>
                  <h2 id="password-title">Смена пароля</h2>
                  <p>Выберите уникальный пароль для своего аккаунта.</p>
                </div>
              </div>
              <form className="settings-form" onSubmit={handlePasswordSubmit}>
                <p id="password-hint" className="settings-hint">Минимум 8 символов. Пароль не должен состоять только из цифр, быть распространённым или похожим на ваши личные данные.</p>
                <div className="settings-field">
                  <label htmlFor="current-password">Текущий пароль</label>
                  <input id="current-password" name="current_password" type="password" autoComplete="current-password" placeholder="Введите текущий пароль" required value={currentPassword} onChange={(event) => setCurrentPassword(event.target.value)} />
                </div>
                <div className="settings-field-grid">
                  <div className="settings-field">
                    <label htmlFor="new-password">Новый пароль</label>
                    <input id="new-password" name="new_password" type="password" autoComplete="new-password" placeholder="Введите новый пароль" required minLength={8} aria-describedby="password-hint" value={newPassword} onChange={(event) => setNewPassword(event.target.value)} />
                  </div>
                  <div className="settings-field">
                    <label htmlFor="confirm-password">Повторите пароль</label>
                    <input id="confirm-password" name="confirm_password" type="password" autoComplete="new-password" placeholder="Ещё раз новый пароль" required value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} />
                  </div>
                </div>
                <div className="settings-actions">
                  <button type="submit" className="settings-secondary">Обновить пароль</button>
                </div>
              </form>
            </section>
          </div>
        </div>
      </div>
    </main>
  );
}
