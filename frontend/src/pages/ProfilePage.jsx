import "../styles/ProfilePage.css";
import Crumbs from "../components/Crumbs";
import { Link } from "react-router-dom";
import { useAuth } from "../components/context/AuthContext";
import { useEffect, useState } from "react";

function ProfilePage() {
    const { user, loading } = useAuth();

    //Работа с данными пользователя
    const [formattedDate, setFormattedDate] = useState('Новый ученик');
    
    

    useEffect(() => {
    const loadRegDate = async () => {
        // ✅ 1. Получаем дату
        const regDate = user?.date_joined;
        
        // ✅ 2. Проверяем, что дата есть
        if (!regDate) {
            setFormattedDate('Новый ученик');
            return;
        }

        // ✅ 3. Создаем объект Date
        const date = new Date(regDate);
        
        // ✅ 4. Проверяем валидность
        if (isNaN(date.getTime())) {
            setFormattedDate('Некорректная дата');
            return;
        }

        // ✅ 5. Форматируем
        const options = { day: "numeric", month: 'long', year: 'numeric' };
        const formatted = new Intl.DateTimeFormat('ru-RU', options).format(date);
        
        // ✅ 6. Сохраняем в state
        setFormattedDate(formatted);
    };

    loadRegDate();
}, [user]);

    const achievments = user?.achievments || [];

    console.log(achievments)
    
    if (loading) {
    return (
      <header className="header">
        <div className="container nav">
          <Link to="/" className="logo">
            <span className="bulb">💡</span>
            Eidos<span>Academy</span>
          </Link>

          <div>Загрузка...</div>
        </div>
      </header>
    );
  }
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

                <h1>{user?.first_name} {user?.last_name}</h1>

                <p>
                  {user?.email}
                </p>

                <span className="profile-member">
                  Ученик с {formattedDate}
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
                <strong>{user?.courses_count}</strong>
                <span>Курса</span>
              </div>

              <div className="profile-stat-card">
                <strong>{user?.topics_count}</strong>
                <span>Уроков пройдено</span>
              </div>

              <div className="profile-stat-card">
                <strong>{achievments.length}</strong>
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
                                                      {/* Progress map!
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
                                                    
                                                      */}
                {/* CURRENT COURSE */}
                {user?.random_course? (<div className="profile-section">
                  <div className="profile-section-header">
                    <div>
                      <span className="profile-section-label">
                        Сейчас изучаете
                      </span>

                      <h2>Ваш случайных курс</h2>
                    </div>
                  </div>

                  <Link
                    to={`/courses/${user?.random_course.id}`}
                    className="profile-course-link"
                    aria-label={`Продолжить курс «${user?.random_course?.title}»`}
                  >
                  <div className="profile-course-card">

                    <div className="profile-course-icon">
                      PY
                    </div>

                    <div className="profile-course-info">
                      <span>{user?.random_course?.category}</span>

                      <h3>{user?.random_course?.title}</h3>

                      <p>
                        {user?.random_course?.short_description}
                      </p>

                      <div className="profile-course-progress">
                        <div className="profile-course-progress-top">
                          <span>Прогресс</span>
                          <strong>{user?.random_course?.progress}%</strong>
                        </div>

                        <div className="profile-progress">
                          <div className="profile-course-progress-bar">
                            <div className="profile-course-progress-fill" style={{ width: `${user?.random_course?.progress || 0}%` }}></div>
                          </div>
                        </div>
                      </div>

                      <span className="profile-course-btn">
                        Продолжить обучение
                        <span aria-hidden="true">→</span>
                      </span>
                    </div>

                  </div>
                  </Link>
                </div>) : (<></>)}
                

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
                                        {achievments.length > 0 ? (
                                            // ✅ Если достижения есть — показываем их
                                            achievments.map((achievment, index) => (
                                                <div className="profile-achievement" key={index}>
                                                    <div className="profile-achievement-icon">
                                                        <img src={`${achievment.icon}`} alt="" />
                                                        
                                                    </div>
                                                    <div>
                                                        <h3>{achievment.title}</h3>
                                                        <p>{achievment.small_description || 'Достижение получено'}</p>
                                                    </div>
                                                </div>
                                            ))
                                        ) : (
                                            // ❌ Если достижений нет — показываем заглушку
                                            <div className="profile-no-achievements">
                                                <p>У вас пока нет достижений</p>
                                                <span>Продолжайте учиться, чтобы их получить!</span>
                                            </div>
                                        )}
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
                      <strong>{user?.first_name} {user?.last_name}</strong>
                    </div>

                    <div className="profile-info-item">
                      <span>Email</span>
                      <strong>{user?.email}</strong>
                    </div>

                    <div className="profile-info-item">
                      <span>Дата регистрации</span>
                      <strong>{formattedDate}</strong>
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
