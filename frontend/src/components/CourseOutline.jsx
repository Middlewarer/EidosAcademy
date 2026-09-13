import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import "../styles/CourseOutline.css";

const labels = { completed: "Пройдена", in_progress: "Начата", not_started: "Не начата" };

export default function CourseOutline({ outline, courseId, moduleId, topicId, progress }) {
  const [expanded, setExpanded] = useState({});
  const [query, setQuery] = useState("");
  const [mobileOpen, setMobileOpen] = useState(false);
  const listRef = useRef(null);
  const activeModule = outline.find((item) => item.id === moduleId);
  const activeTopic = activeModule?.topics.find((item) => item.id === topicId);
  const term = query.trim().toLocaleLowerCase();
  useEffect(() => {
    setExpanded((current) => ({ ...current, [moduleId]: true }));
    setMobileOpen(false);
  }, [moduleId, topicId]);
  const matches = outline.map((item) => ({ ...item, topics: item.topics.filter((topic) =>
    !term || topic.title.toLocaleLowerCase().includes(term) || item.title.toLocaleLowerCase().includes(term))
  })).filter((item) => !term || item.topics.length);
  const locate = () => {
    setQuery("");
    setExpanded((current) => ({ ...current, [moduleId]: true }));
    requestAnimationFrame(() => {
      const list = listRef.current;
      const link = list?.querySelector('[aria-current="page"]');
      if (link) list.scrollTop += link.getBoundingClientRect().top - list.getBoundingClientRect().top - 60;
    });
  };
  return (
    <aside className="study-outline" aria-label="Содержание курса">
      <button type="button" className="study-mobile-toggle" aria-expanded={mobileOpen}
        aria-controls="study-outline-body" onClick={() => setMobileOpen(!mobileOpen)}>
        <span><strong>Содержание курса</strong><small>{activeTopic?.title || "Выберите тему"}</small></span>
        <span aria-hidden="true">{mobileOpen ? "−" : "+"}</span>
      </button>
      <div id="study-outline-body" className={`study-outline-body ${mobileOpen ? "is-open" : ""}`}>
        <div className="study-outline-head">
          <div><h2>Содержание курса</h2><strong>{progress?.percent ?? 0}%</strong></div>
          <progress value={progress?.completed_topics ?? 0} max={progress?.total_topics || 1} aria-label="Прогресс курса" />
          <p>{progress?.completed_topics ?? 0} из {progress?.total_topics ?? 0} тем пройдено</p>
          <label className="study-search"><span className="study-sr">Поиск темы</span>
            <input type="search" placeholder="Найти тему…" value={query} onChange={(event) => setQuery(event.target.value)} />
          </label>
          <button className="study-locate" type="button" onClick={locate}>К текущей теме ↓</button>
        </div>
        <div className="study-outline-scroll" ref={listRef}>
          {matches.length ? matches.map((item) => {
            const allTopics = outline.find((original) => original.id === item.id).topics;
            const done = allTopics.filter((topic) => topic.status === "completed").length;
            const isOpen = !!term || (expanded[item.id] ?? item.id === moduleId);
            return <section className="study-module" key={item.id}>
              <button className="study-module-toggle" type="button" aria-expanded={isOpen} aria-controls={`study-module-${item.id}`}
                onClick={() => setExpanded((current) => ({ ...current, [item.id]: !isOpen }))}>
                <span className="study-chevron" aria-hidden="true">{isOpen ? "⌄" : "›"}</span>
                <span><strong>{item.title}</strong><small>{allTopics.length ? `${done} / ${allTopics.length} пройдено` : "Тем пока нет"}</small></span>
                {allTopics.length > 0 && done === allTopics.length && <span className="study-done" aria-label="Модуль пройден">✓</span>}
              </button>
              <ol id={`study-module-${item.id}`} hidden={!isOpen}>
                {item.topics.map((topic) => <li key={topic.id}>
                  <Link to={`/courses/${courseId}/modules/${item.id}?topic=${topic.id}`}
                    aria-current={topic.id === topicId ? "page" : undefined} className={`study-topic is-${topic.status}`}
                    onClick={() => setMobileOpen(false)}>
                    <span className="study-topic-mark" aria-hidden="true">{topic.status === "completed" ? "✓" : topic.id === topicId ? "•" : ""}</span>
                    <span>{topic.title}</span><span className="study-sr"> — {labels[topic.status]}</span>
                  </Link>
                </li>)}
              </ol>
            </section>;
          }) : <p className="study-no-results">{term ? "По этому запросу тем нет." : "Содержание ещё готовится."}</p>}
        </div>
        <div className="study-legend"><span>✓ Пройдено</span><span>● Текущая тема</span></div>
      </div>
    </aside>
  );
}
