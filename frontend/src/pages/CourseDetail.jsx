import "../styles/CourseDetail.css";
import Crumbs from "../components/Crumbs";
import { useEffect, useState } from "react";
import Module from "../components/course_detail/Module";
import { useParams } from "react-router-dom";
import {Link } from "react-router-dom"

function CourseDetail() {
    const [course, setCourse] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    const [moduleCounter, setModuleCounter] = useState(0)

    const [topicCounter, setTopicCounter] = useState(0)

    const [modules, setModules] = useState([])

    const { id } = useParams();

    const getCourse = async () => {
        try {
            setLoading(true)
            setError(null)

            const response = await fetch(`http://127.0.0.1:8000/api/courses/${id}/`)
            const data = await response.json()

            if (!response.ok || !data.course) {
                setCourse(null)
                setModules([])
                setError(data.reason || "Не удалось загрузить курс")
                return
            }

            setModuleCounter(data.module_counter ?? 0)
            setTopicCounter(data.topic_counter ?? 0)
            setCourse(data.course)
            setModules(data.course.modules ?? [])
        } catch {
            setCourse(null)
            setModules([])
            setError("Не удалось загрузить курс")
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        if (!id) {
            return;
        }

        getCourse();
    }, [id]);

    if (loading) {
        return (
            <div className="course-detail-page">
                <main>
                    <Crumbs />
                    <div className="container">
                        <p>Загрузка курса...</p>
                    </div>
                </main>
            </div>
        );
    }

    if (error || !course) {
        return (
            <div className="course-detail-page">
                <main>
                    <Crumbs />
                    <div className="container">
                        <p>{error || "Курс не найден"}</p>
                    </div>
                </main>
            </div>
        );
    }

  return (
    <div className="course-detail-page">
      <main>
        {/* Хлебные крошки + назад */}
        < Crumbs/>

        {/* Шапка курса */}
        <section className="course-detail-hero">
          <div className="container course-detail-hero-grid">
            <div className="course-detail-info">
              <span className="course-detail-label">Python</span>

              <h1>{course.title}</h1>

              <p className="course-detail-description">
                {course.short_description}
              </p>

              <div className="course-detail-meta">
                <div>
                  <strong>{moduleCounter}</strong>
                  <span>модулей</span>
                </div>
                <div>
                  <strong>{topicCounter}</strong>
                  <span>уроков</span>
                </div>
                <div>
                  <strong>~20 ч</strong>
                  <span>обучения</span>
                </div>
              </div>

              {modules[0] && (
                <Link to={`/courses/${id}/modules/${modules[0].id}`}>
                  <button type="button" className="course-detail-start-btn">
                    Начать обучение
                  </button>
                </Link>
              )}
            </div>

            <div className="course-detail-cover">
              <div className="course-detail-cover-icon">PY</div>
              <p>Обложка курса</p>
            </div>
          </div>
        </section>

        {/* Чему научитесь */}
        <section className="course-detail-learn">
          <div className="container">
            <h2>Чему вы научитесь</h2>

            <ul className="course-detail-learn-list">
              <li>Писать программы на Python с нуля</li>
              <li>Работать с переменными, условиями и циклами</li>
              <li>Создавать и использовать функции</li>
              <li>Читать и записывать файлы</li>
              <li>Решать практические задачи после каждого модуля</li>
            </ul>
          </div>
        </section>

        {/* Программа курса */}
        <section className="course-detail-program">
          <div className="container">
            <h2>Программа курса</h2>

            <div className="course-detail-modules">
              {modules.map((module) => (
                <Module
                  key={module.id}
                  id={module.id}
                  courseId={id}
                  title={module.title}
                  topics={module.topics}
                />
              ))}
            </div>
          </div>
        </section>

        {/* CTA внизу */}
        <section className="course-detail-cta">
          <div className="container">
            <h2>Готовы начать?</h2>
            <p>Присоединяйтесь к курсу и начните учиться уже сегодня.</p>
            {modules[0] && (
              <Link to={`/courses/${id}/modules/${modules[0].id}`}>
                <button type="button" className="course-detail-start-btn">
                  Начать обучение
                </button>
              </Link>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default CourseDetail;