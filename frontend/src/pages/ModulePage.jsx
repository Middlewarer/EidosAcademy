import "../styles/ModulePage.css";
import MarkdownContent from "../components/MarkdownContent";
import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";

function ModulePage() {

    const {courseId, moduleId} = useParams();

    const [selectedTopicId, setSelectedTopicId] = useState(null);

    const [module, setModule] = useState(null)

    const getModule = async () => {
      const response = await fetch(`http://127.0.0.1:8000/api/modules/${moduleId}`)
      const data = await response.json();
      return data
    }

    const handleTopicClick = (topicId) => {
        setSelectedTopicId(topicId);
        console.log("Выбран топик с Id", topicId)
    }

    useEffect(() => {
      const loadModule = async () => {
        const data = await getModule();
        console.log(data)
        setModule(data.module)

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

  return (
    <div className="module-page">
      <main>
        <section className="module-page-top">
          <div className="container">
            <Link to={`/courses/`} className="module-page-back">
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
              <span>{selectedTopic?.order + 1} из {module?.topics?.length}</span>
            </div>
          </div>
        </section>

        <section className="module-page-content">
          <div className="container module-page-grid">
            <aside className="module-page-">
              <h2>Уроки модуля</h2>

              <ul className="module-page-topics">
                {module?.topics?.map((topic) => (<li key={topic.id}
                onClick={() => handleTopicClick(topic.id)}
                className={topic.id === selectedTopicId ? "is-active" : ""}

                >
                    <span className="module-page-topic-number">
                        {topic.order + 1}
                    </span>

                    <div>
                      <strong>{topic.title}</strong>
                    </div>
                  </li>))}
              </ul>
            </aside>

            <article className="module-page-lesson">
              <span className="module-page-lesson-type">
                Урок {selectedTopic?.order + 1} | {selectedTopic?.title} 
              </span>

              <MarkdownContent content={selectedLesson?.content}/>
            </article>
          </div>
        </section>
      </main>
    </div>
  );
}

export default ModulePage;
