import "../styles/CourseDetail.css";
import Crumbs from "../components/Crumbs";
import { useCallback, useEffect, useState } from "react";
import Module from "../components/course_detail/Module";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../components/context/AuthContext";
import { apiRequest } from "../components/api/apiRequest";

function CourseDetail() {
  const navigate = useNavigate();
    const [course, setCourse] = useState(null)
    const [error, setError] = useState(null)
    const { user, loading } = useAuth()
    const [modules, setModules] = useState([])
    const [continueModuleId, setContinueModuleId] = useState(null);
    const [isAssigned, setIsAssigned] = useState(false);
    const [isAssigning, setIsAssigning] = useState(false);
    const [assignError, setAssignError] = useState(null);

    const { courseId } = useParams();

    const getCourse = useCallback(async () => {
        const response = await apiRequest(`/api/courses/${courseId}/`)
        if (!response.ok) {
          throw new Error("Не удалось загрузить курс.");
        }
        const data = await response.json()
        return data
    }, [courseId]);

    const handleCourseAction = async () => {
      if (!modules[0] || isAssigning) return;

      const targetModuleId = continueModuleId || modules[0].id;

      if (isAssigned) {
        navigate(`/courses/${courseId}/modules/${targetModuleId}`);
        return;
      }

      setIsAssigning(true);
      setAssignError(null);

      try {
        const response = await apiRequest("/api/assign/", {
          method: "POST",
          body: JSON.stringify({ course_id: course.course_id }),
        });

        if (!response.ok) {
          const data = await response.json().catch(() => ({}));
          throw new Error(data.error || "Не удалось начать обучение.");
        }

        setIsAssigned(true);
        setContinueModuleId(modules[0].id);
        navigate(`/courses/${courseId}/modules/${modules[0].id}`);
      } catch (err) {
        setAssignError(err.message);
      } finally {
        setIsAssigning(false);
      }
    };

    useEffect(() => {
    const loadCourse = async () => {
        try {
            const data = await getCourse();  // Здесь приходит ВЕСЬ ответ
            
            // Сохраняем курс
            setCourse(data);
            setIsAssigned(data.is_assigned);
            setContinueModuleId(data.continue_module_id);
            
            // Сохраняем модули (они внутри course)
            setModules(data.course.modules || []);
            
        } catch (err) {
            setError(err.message);
        }
    };
    
    loadCourse();
}, [getCourse]);

  if (loading) return <p role="status">Загрузка курса…</p>;
  if (error) return <p role="alert">{error}</p>;
  if (user) {
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
                <button type="button" className="course-detail-start-btn" onClick={handleCourseAction} disabled={isAssigning}>
                  {isAssigning ? "Добавляем курс…" : isAssigned ? "Вернуться к курсу" : "Начать обучение"}
                </button>
              )}
              {modules.length === 0 && <p>В этом курсе пока нет модулей.</p>}
              {assignError && <p role="alert">{assignError}</p>}
            </div>

            <div className={`course-detail-cover ${course?.course?.image ? "has-image" : ""}`}>
              {course?.course?.image ? (
                <img src={course.course.image} alt={`Обложка курса «${course.course.title}»`} />
              ) : (
                <><div className="course-detail-cover-icon">{course?.course?.title?.charAt(0) || "E"}</div><p>Обложка скоро появится</p></>
              )}
            </div>
          </div>
        </section>

        {/* Чему научитесь */}
        {/*<section className="course-detail-learn">
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
        </section> */}

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
            <h2>{isAssigned ? "Продолжим обучение?" : "Готовы начать?"}</h2>
            <p>{isAssigned
              ? "Вернитесь к последнему открытому модулю."
              : "Присоединяйтесь к курсу и начните учиться уже сегодня."}</p>
            {modules[0] && (
              <button type="button" className="course-detail-start-btn" onClick={handleCourseAction} disabled={isAssigning}>
                {isAssigning ? "Добавляем курс…" : isAssigned ? "Вернуться к курсу" : "Начать обучение"}
              </button>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

return (
  <div>Загрузка...</div>
)
}

export default CourseDetail;
