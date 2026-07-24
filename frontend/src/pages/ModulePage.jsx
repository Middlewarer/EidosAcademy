import "../styles/ModulePage.css";
import MarkdownContent from "../components/MarkdownContent";
import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";

function ModulePage() {
  const [module, setModule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedTopic, setSelectedTopic] = useState(0);

  const { courseId, moduleId } = useParams();

  useEffect(() => {
    if (!moduleId) {
      return;
    }

    const getModule = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(
          `http://127.0.0.1:8000/api/modules/${moduleId}`
        );
        const data = await response.json();

        if (!response.ok || !data.module) {
          setModule(null);
          setError("Не удалось загрузить модуль");
          return;
        }

        setModule(data.module);
        setSelectedTopic(0);
      } catch {
        setModule(null);
        setError("Не удалось загрузить модуль");
      } finally {
        setLoading(false);
      }
    };

    getModule();
  }, [moduleId]);

  if (loading) {
    return (
      <div className="module-page">
        <main>
          <div className="container">
            <p>Загрузка модуля...</p>
          </div>
        </main>
      </div>
    );
  }

  if (error || !module) {
    return (
      <div className="module-page">
        <main>
          <div className="container">
            <Link to={`/courses/${courseId}`} className="module-page-back">
              ← Назад к курсу
            </Link>
            <p>{error || "Модуль не найден"}</p>
          </div>
        </main>
      </div>
    );
  }

  const topics = module.topics ?? [];
  const selectedLesson = topics[selectedTopic]?.lessons?.[0];

  return (
    <div className="module-page">
      <main>
        <section className="module-page-top">
          <div className="container">
            <Link to={`/courses/${courseId}`} className="module-page-back">
              ← Назад к курсу
            </Link>

            <div className="module-page-breadcrumbs">
              <span>{module.course_title}</span>
              <span>/</span>
              <span>{module.title}</span>
            </div>
          </div>
        </section>

        <section className="module-page-header">
          <div className="container">
            <span className="module-page-label">Модуль {module.order}</span>
            <h1>{module.title}</h1>
            <p>{module.description}</p>

            <div className="module-page-progress">
              <div className="module-page-progress-bar">
                <div className="module-page-progress-fill"></div>
              </div>
              <span>0 из {topics.length} уроков пройдено</span>
            </div>
          </div>
        </section>

        <section className="module-page-content">
          <div className="container module-page-grid">
            <aside className="module-page-sidebar">
              <h2>Уроки модуля</h2>

              <ul className="module-page-topics">
                {topics.map((topic, index) => (
                  <li
                    key={topic.id}
                    className={selectedTopic === index ? "is-active" : ""}
                    onClick={() => setSelectedTopic(index)}
                  >
                    <span className="module-page-topic-number">
                      {index + 1}
                    </span>

                    <div>
                      <strong>{topic.title}</strong>
                    </div>
                  </li>
                ))}
              </ul>
            </aside>

            <article className="module-page-lesson">
              <span className="module-page-lesson-type">
                Урок {selectedTopic + 1} · Markdown
              </span>

              <MarkdownContent content={selectedLesson?.content || ""} />
            </article>
          </div>
        </section>
      </main>
    </div>
  );
}

export default ModulePage;
