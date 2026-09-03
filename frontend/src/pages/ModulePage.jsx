import "../styles/ModulePage.css";
import MarkdownContent from "../components/MarkdownContent";
import { useParams, Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function ModulePage() {

    const {courseId, moduleId} = useParams();
    const navigate = useNavigate();

    const [selectedTopicId, setSelectedTopicId] = useState(null);
    const [module, setModule] = useState(null);
    const [nextModuleId, setNextModuleId] = useState(null);

    const getModule = async () => {
      const response = await fetch(`http://127.0.0.1:8000/api/modules/${moduleId}`)
      const data = await response.json();
      return data
    }

      const topics = module?.topics ?? [];
    const selectedTopicIndex = topics.findIndex(
  (topic) => topic.id === selectedTopicId
);
    
    const previousTopic = selectedTopicIndex > 0 ? topics[selectedTopicIndex - 1] ?? null : null;
    const nextTopic =
  selectedTopicIndex >= 0
    ? topics[selectedTopicIndex + 1] ?? null
    : null;

    const selectTopic = (topic) => {
  if (!topic) return;

  setSelectedTopicId(topic.id);

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
};

const handlePreviousTopic = () => {
  selectTopic(previousTopic);
};

const handleNextTopic = () => {
  selectTopic(nextTopic);
};

    const handleTopicClick = (topicId) => {
        setSelectedTopicId(topicId);
        console.log("Выбран топик с Id", topicId)
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    const handleNextModule = () => {
        if (nextModuleId) {
            navigate(`/courses/${courseId}/modules/${nextModuleId}`);
        }
    }

    useEffect(() => {
      const loadModule = async () => {
        const data = await getModule();
        console.log(data)
        setModule(data.module)
        setNextModuleId(data.module.next_module_id || null)

          if (data.module?.topics?.length > 0) {
            setSelectedTopicId(data.module.topics[0].id)
          }
      }
      loadModule();
    }, [moduleId])

    const selectedTopic = module?.topics?.find(
    topic => topic.id === selectedTopicId
    );

    const selectedLesson = selectedTopic?.lessons?.[0];

    const isLastTopic = module?.topics && selectedTopic?.id === module.topics[module.topics.length - 1]?.id;

  return (
    <div className="module-page">
      <main>
        <section className="module-page-top">
          <div className="container">
            <Link to={`/courses/${courseId}`} className="module-page-back">
              ← Назад к курсу
            </Link>

            <div className="module-page-breadcrumbs">
              <span>{module?.course_title}</span>
              <span>/</span>
              <span>{module?.title}</span>
            </div>
          </div>
        </section>

        <section className="module-page-header">
          <div className="container">
            <span className="module-page-label">{selectedTopic?.title}</span>
            <h1>{module?.title}</h1>
            <p>{module?.description}</p>

            <div className="module-page-progress">
              <div className="module-page-progress-bar">
                <div className="module-page-progress-fill" style={{width: `${100 / module?.topics?.length * (selectedTopic?.order + 1)}%`}}></div>
              </div>
              <span>{selectedTopic? selectedTopic?.order + 1 : 0} из {module?.topics?.length}</span>
            </div>
          </div>
        </section>

        <section className="module-page-content">
          <div className="container module-page-grid">
            <aside className="module-page-topics-sidebar">
              <h2>Уроки модуля</h2>

              <ul className="module-page-topics">
                {module?.topics?.map((topic) => (<li
                  key={topic.id}
                  className={topic.id === selectedTopicId ? "is-active" : ""}
                >
                  <button
                    type="button"
                    onClick={() => handleTopicClick(topic.id)}
                    aria-current={topic.id === selectedTopicId ? "step" : undefined}
                  >
                    <span className="module-page-topic-number">
                        {topic.order + 1}
                    </span>

                    <div>
                      <strong>{topic.title}</strong>
                    </div>
                  </button>
                </li>))}
              </ul>

              {/* Кнопка перехода на следующий модуль */}
              {nextModuleId && isLastTopic && (
                <div className="module-page-next-module">
                  <button 
                    onClick={handleNextModule}
                    className="next-module-button"
                  >
                    Перейти на следующий модуль →
                  </button>
                </div>
              )}
            </aside>

            <article className="module-page-lesson">
              
                {selectedTopic? <span className="module-page-lesson-type">Урок {selectedTopic?.order + 1} | {selectedTopic?.title}</span> : <p>Выбери урок</p>} 
              
              {selectedLesson? <MarkdownContent content={selectedLesson?.content}/> : <p>Выбери топик</p>}

              <nav className="lesson-navigation" aria-label="Навигация между топиками">
                <button
                  type="button"
                  className="lesson-navigation-button lesson-navigation-button--previous"
                  data-direction="previous"
                  onClick={handlePreviousTopic}
                  disabled={!previousTopic}
                >
                  <span className="lesson-navigation-arrow" aria-hidden="true">←</span>
                  <span className="lesson-navigation-copy">
                    <small>Предыдущий топик</small>
                    <strong>Вернуться назад</strong>
                  </span>
                </button>

                <button
                    type="button"
                    className="lesson-navigation-button lesson-navigation-button--next"
                    onClick={handleNextTopic}
                    disabled={!nextTopic}
                  >
                  <span className="lesson-navigation-copy">
                    <small>Следующий топик</small>
                    <strong>Продолжить обучение</strong>
                  </span>
                  <span className="lesson-navigation-arrow" aria-hidden="true">→</span>
                </button>
              </nav>

              {nextModuleId && isLastTopic && (
                <div className="module-page-next-module">
                  <button
                    onClick={handleNextModule}
                    className="next-module-button"
                  >
                    Перейти на следующий модуль →
                  </button>
                </div>
              )}
            </article>
          </div>
        </section>
      </main>
    </div>
    
  );
}

export default ModulePage;
