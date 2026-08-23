import "../styles/ModulePage.css";
import MarkdownContent from "../components/MarkdownContent";
import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";

function ModulePage() {

  const {courseId, moduleId} = useParams();

  const fetchData = () => {
    const response = fetch("https://127.0.0.1:8000/api/courses")
  }

  return (
    <div className="module-page">
      <main>
        <section className="module-page-top">
          <div className="container">
            <Link to={`/courses/`} className="module-page-back">
              ← Назад к курсу
            </Link>

            <div className="module-page-breadcrumbs">
              <span>Название курса</span>
              <span>/</span>
              <span>Название модуля</span>
            </div>
          </div>
        </section>

        <section className="module-page-header">
          <div className="container">
            <span className="module-page-label">Модуль порядок модуля</span>
            <h1>Название модуля</h1>
            <p>Описание модуля</p>

            <div className="module-page-progress">
              <div className="module-page-progress-bar">
                <div className="module-page-progress-fill"></div>
              </div>
              <span>0 из 1</span>
            </div>
          </div>
        </section>

        <section className="module-page-content">
          <div className="container module-page-grid">
            <aside className="module-page-">
              <h2>Уроки модуля</h2>

              <ul className="module-page-topics">
                  <li>
                    <span className="module-page-topic-number">
                        1
                    </span>

                    <div>
                      <strong>Название топика</strong>
                    </div>
                  </li>
                  <li>
                    <span className="module-page-topic-number">
                        1
                    </span>

                    <div>
                      <strong>Название топика</strong>
                    </div>
                  </li>
                  <li>
                    <span className="module-page-topic-number">
                        1
                    </span>

                    <div>
                      <strong>Название топика</strong>
                    </div>
                  </li>
                  <li>
                    <span className="module-page-topic-number">
                        1
                    </span>

                    <div>
                      <strong>Название топика</strong>
                    </div>
                  </li>
              </ul>
            </aside>

            <article className="module-page-lesson">
              <span className="module-page-lesson-type">
                Урок 1 · Markdown
              </span>

              <MarkdownContent />
            </article>
          </div>
        </section>
      </main>
    </div>
  );
}

export default ModulePage;
