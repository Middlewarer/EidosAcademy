import "../styles/ModulePage.css";
import MarkdownContent from "../components/MarkdownContent";
import lessonMarkdown from "../content/lessons/python-intro.md?raw";
import { useEffect, useState } from "react"

function ModulePage() {

  const [topics, setTopics] = useState([])
  const [selectedTopic, setSelectedTopic] = useState(0);

  const getTopics = async () => {
    const response = await fetch("http://127.0.0.1:8000/api/modules/1")
    const data = await response.json()

    setTopics(data.module.topics)
  }

  useEffect(() => {
    getTopics();
  }, []) 
  return (
    <div className="module-page">
      <main>
        <section className="module-page-top">
          <div className="container">
            <a href="/details" className="module-page-back">
              ← Назад к курсу
            </a>

            <div className="module-page-breadcrumbs">
              <span>Python для начинающих</span>
              <span>/</span>
              <span>Модуль 1</span>
            </div>
          </div>
        </section>

        <section className="module-page-header">
          <div className="container">
            <span className="module-page-label">Модуль 1 из 4</span>
            <h1>Введение в Python</h1>
            <p>
              Знакомство с языком, установка окружения и первая программа.
              В этом модуле вы поймёте, зачем нужен Python и как начать с ним
              работать.
            </p>

            <div className="module-page-progress">
              <div className="module-page-progress-bar">
                <div className="module-page-progress-fill"></div>
              </div>
              <span>1 из 3 уроков пройдено</span>
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
    className={selectedTopic === index ? "active" : ""}
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
              <span className="module-page-lesson-type">Урок 1 · Markdown</span>
                
                <MarkdownContent
    content={topics[selectedTopic]?.lessons[0]?.content || ""}
/>
              
            </article>
          </div>
        </section>
      </main>
    </div>
  );
}

export default ModulePage;
