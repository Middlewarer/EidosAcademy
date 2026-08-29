import "../styles/ProfilePage.css";
import Crumbs from "../components/Crumbs";
import { Link } from "react-router-dom";

function ProfilePage() {
  return (
    <div className="profile-page">
      <main>
        <Crumbs />

        {/* PROFILE HERO */}
        <section className="profile-hero">
          <div className="container">
            <div className="profile-hero-card">
              
              <div className="profile-avatar">
                A
              </div>

              <div className="profile-main-info">
                <span className="profile-label">Профиль ученика</span>

                <h1>Александр Иванов</h1>

                <p>
                  alexander@example.com
                </p>

                <span className="profile-member">
                  Ученик с августа 2026
                </span>
              </div>

              <Link to="/settings">
                <button className="profile-edit-btn">
                  Редактировать профиль
                </button>
              </Link>

            </div>
          </div>
        </section>

        {/* STATISTICS */}
        <section className="profile-stats">
          <div className="container">
            <div className="profile-stats-grid">

              <div className="profile-stat-card">
                <strong>3</strong>
                <span>Курса</span>
              </div>

              <div className="profile-stat-card">
                <strong>18</strong>
                <span>Уроков пройдено</span>
              </div>

              <div className="profile-stat-card">
                <strong>7</strong>
                <span>Часов обучения</span>
              </div>

              <div className="profile-stat-card">
                <strong>4</strong>
                <span>Достижения</span>
              </div>

            </div>
          </div>
        </section>

        {/* CONTENT */}
        <section className="profile-content">
          <div className="container">
            <div className="profile-content-grid">

              {/* LEFT */}
              <div className="profile-left">

                {/* PROGRESS */}
                <div className="profile-section">
                  <div className="profile-section-header">
                    <div>
                      <span className="profile-section-label">
                        Обучение
                      </span>

                      <h2>Ваш прогресс</h2>
                    </div>

                    <span className="profile-progress-percent">
                      65%
                    </span>
                  </div>

                  <div className="profile-progress">
                    <div className="profile-progress-bar">
                      <div className="profile-progress-fill"></div>
                    </div>
                  </div>

                  <p className="profile-progress-text">
                    Вы уже прошли большую часть текущего курса.
                    Продолжайте в том же духе!
                  </p>
                </div>

                {/* CURRENT COURSE */}
                <div className="profile-section">
                  <div className="profile-section-header">
                    <div>
                      <span className="profile-section-label">
                        Сейчас изучаете
                      </span>

                      <h2>Мои курсы</h2>
                    </div>
                  </div>

                  <div className="profile-course-card">

                    <div className="profile-course-icon">
                      PY
                    </div>

                    <div className="profile-course-info">
                      <span>Программирование</span>

                      <h3>Python с нуля</h3>

                      <p>
                        Основы Python, переменные, условия,
                        циклы и функции.
                      </p>

                      <div className="profile-course-progress">
                        <div className="profile-course-progress-top">
                          <span>Прогресс</span>
                          <strong>65%</strong>
                        </div>

                        <div className="profile-progress">
                          <div className="profile-course-progress-bar">
                            <div className="profile-course-progress-fill"></div>
                          </div>
                        </div>
                      </div>

                      <Link
                        to="/courses/1"
                        className="profile-course-btn"
                      >
                        Продолжить обучение
                      </Link>
                    </div>

                  </div>
                </div>

                {/* ACHIEVEMENTS */}
                <div className="profile-section">
                  <div className="profile-section-header">
                    <div>
                      <span className="profile-section-label">
                        Ваши успехи
                      </span>

                      <h2>Достижения</h2>
                    </div>
                  </div>

                  <div className="profile-achievements">

                    <div className="profile-achievement">
                      <div className="profile-achievement-icon">
                        ★
                      </div>

                      <div>
                        <h3>Первый шаг</h3>
                        <p>
                          Вы прошли первый урок
                        </p>
                      </div>
                    </div>

                    <div className="profile-achievement">
                      <div className="profile-achievement-icon">
                        ✓
                      </div>

                      <div>
                        <h3>В ритме</h3>
                        <p>
                          7 дней обучения подряд
                        </p>
                      </div>
                    </div>

                    <div className="profile-achievement">
                      <div className="profile-achievement-icon">
                        &lt;/&gt;
                      </div>

                      <div>
                        <h3>Программист</h3>
                        <p>
                          Пройдено 10 уроков
                        </p>
                      </div>
                    </div>

                    <div className="profile-achievement">
                      <div className="profile-achievement-icon">
                        ★
                      </div>

                      <div>
                        <h3>Отличник</h3>
                        <p>
                          Все задания выполнены
                        </p>
                      </div>
                    </div>

                  </div>
                </div>

              </div>

              {/* RIGHT */}
              <aside className="profile-sidebar">

                {/* ABOUT */}
                <div className="profile-side-card">
                  <span className="profile-section-label">
                    Личная информация
                  </span>

                  <h2>О вас</h2>

                  <div className="profile-info-list">

                    <div className="profile-info-item">
                      <span>Имя</span>
                      <strong>Александр Иванов</strong>
                    </div>

                    <div className="profile-info-item">
                      <span>Email</span>
                      <strong>alexander@example.com</strong>
                    </div>

                    <div className="profile-info-item">
                      <span>Дата регистрации</span>
                      <strong>12 августа 2026</strong>
                    </div>

                    <div className="profile-info-item">
                      <span>Уровень</span>
                      <strong>Начинающий</strong>
                    </div>

                  </div>
                </div>

                {/* ACTIVITY */}
                <div className="profile-side-card">
                  <span className="profile-section-label">
                    Активность
                  </span>

                  <h2>Последние действия</h2>

                  <div className="profile-activity">

                    <div className="profile-activity-item">
                      <div className="profile-activity-dot"></div>

                      <div>
                        <strong>Урок завершён</strong>
                        <span>
                          Переменные в Python
                        </span>
                        <small>
                          Сегодня
                        </small>
                      </div>
                    </div>

                    <div className="profile-activity-item">
                      <div className="profile-activity-dot"></div>

                      <div>
                        <strong>Получено достижение</strong>
                        <span>
                          В ритме
                        </span>
                        <small>
                          Вчера
                        </small>
                      </div>
                    </div>

                    <div className="profile-activity-item">
                      <div className="profile-activity-dot"></div>

                      <div>
                        <strong>Урок завершён</strong>
                        <span>
                          Условия и логика
                        </span>
                        <small>
                          2 дня назад
                        </small>
                      </div>
                    </div>

                  </div>
                </div>

              </aside>

            </div>
          </div>
        </section>

        {/* BOTTOM CTA */}
        <section className="profile-cta">
          <div className="container">
            <div className="profile-cta-card">

              <div>
                <span className="profile-section-label">
                  Не останавливайтесь
                </span>

                <h2>
                  Продолжайте учиться
                </h2>

                <p>
                  Каждый новый урок приближает вас к цели.
                </p>
              </div>

              <Link to="/courses">
                <button className="profile-cta-btn">
                  Перейти к курсам
                </button>
              </Link>

            </div>
          </div>
        </section>

      </main>
    </div>
  );
}

export default ProfilePage;