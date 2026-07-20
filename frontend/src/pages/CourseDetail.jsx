import "../styles/CourseDetail.css";
import Crumbs from "../components/Crumbs";
import { useEffect, useState } from "react";
import Module from "../components/course_detail/Module";

function CourseDetail() {
    const [course, setCourse] = useState({})

    const [moduleCounter, setModuleCounter] = useState(1)

    const [topicCounter, setTopicCounter] = useState(1)

    const [modules, setModules] = useState([])

    const getCourse = async () => {
        const response = await fetch("http://127.0.0.1:8000/api/courses/1/")
        const course = await response.json()

        
        setModuleCounter(course.module_counter)
        setTopicCounter(course.topic_counter)
        setCourse(course.course);
        setModules(course.course.modules)
    }

    useEffect(() => {getCourse()}, [])

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

              <button type="button" className="course-detail-start-btn">
                Начать обучение
              </button>
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
    <Module title={module.title} topics={module.topics}/>
))}
            </div>
          </div>
        </section>

        {/* CTA внизу */}
        <section className="course-detail-cta">
          <div className="container">
            <h2>Готовы начать?</h2>
            <p>Присоединяйтесь к курсу и начните учиться уже сегодня.</p>
            <button type="button" className="course-detail-start-btn">
              Начать обучение
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default CourseDetail;