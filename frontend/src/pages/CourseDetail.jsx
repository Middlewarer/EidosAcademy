import "../styles/CourseDetail.css";
import Crumbs from "../components/Crumbs";
import { useEffect, useState } from "react";
import Module from "../components/course_detail/Module";
import { useParams } from "react-router-dom";
import {Link } from "react-router-dom"

function CourseDetail() {
    const [course, setCourse] = useState(null)
    const [error, setError] = useState(null)

    const [modules, setModules] = useState([])

    const { courseId } = useParams();

    const getCourse = async () => {
        const response = await fetch(`http://127.0.0.1:8000/api/courses/${courseId}/`)
        const data = await response.json()
        console.log(data)
        return data
    }

    useEffect(() => {
    const loadCourse = async () => {
        try {
            const data = await getCourse();  // Здесь приходит ВЕСЬ ответ
            
            // Сохраняем курс
            setCourse(data);
            
            // Сохраняем модули (они внутри course)
            setModules(data.course.modules || []);
            
        } catch (err) {
            setError(err.message);
        }
    };
    
    loadCourse();
}, [courseId]);

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

              <h1>{course?.course?.title}</h1>

              <p className="course-detail-description">
                {course?.course?.short_description}
              </p>

              <div className="course-detail-meta">
                <div>
                  <strong>{course?.module_counter}</strong>
                  <span>модулей</span>
                </div>
                <div>
                  <strong>{course?.topic_counter}</strong>
                  <span>уроков</span>
                </div>
                <div>
                  <strong>~20 ч</strong>
                  <span>обучения</span>
                </div>
              </div>

              {modules[0] && (
                <Link to={`/courses/${courseId}/modules/${modules[0].id}`}>
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
                  courseId={courseId}
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
              <Link to={`/courses/${courseId}/modules/${modules[0].id}`}>
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