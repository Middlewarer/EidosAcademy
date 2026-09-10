import "../styles/ModulePage.css";
import MarkdownContent from "../components/MarkdownContent";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useCallback, useEffect, useMemo, useState } from "react";
import { apiRequest } from "../components/api/apiRequest";

const STATUS_LABELS = { not_started: "Не начат", in_progress: "В процессе", completed: "Пройден" };

function updateOutlineTopic(outline, topicId, status) {
  return outline.map((moduleItem) => {
    const topics = moduleItem.topics.map((topic) => topic.id === topicId ? { ...topic, status } : topic);
    const moduleStatus = topics.length && topics.every((topic) => topic.status === "completed")
      ? "completed"
      : topics.some((topic) => topic.status !== "not_started") ? "in_progress" : "not_started";
    return { ...moduleItem, topics, status: moduleStatus };
  });
}

function ModulePage() {
  const { courseId, moduleId } = useParams();
  const navigate = useNavigate();
  const [selectedTopicId, setSelectedTopicId] = useState(null);
  const [module, setModule] = useState(null);
  const [outline, setOutline] = useState([]);
  const [courseProgress, setCourseProgress] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isCompleting, setIsCompleting] = useState(false);
  const [error, setError] = useState(null);
  const [progressError, setProgressError] = useState(null);

  const getModule = useCallback(async () => {
    const response = await apiRequest(`/api/modules/${moduleId}/`);
    if (!response.ok) throw new Error(`Не удалось загрузить модуль: ${response.status}`);
    return response.json();
  }, [moduleId]);

  const saveTopicVisit = useCallback(async (topicId) => {
    const response = await apiRequest("/api/progress/visit/", {
      method: "POST",
      body: JSON.stringify({ topic: topicId }),
    });
    if (!response.ok) throw new Error("Не удалось сохранить последнее открытое место.");
    return response.json();
  }, []);

  const markTopicStatus = useCallback((topicId, status) => {
    setModule((current) => current ? {
      ...current,
      topics: current.topics.map((topic) => topic.id === topicId ? { ...topic, status } : topic),
    } : current);
    setOutline((current) => updateOutlineTopic(current, topicId, status));
  }, []);

  const openTopic = async (destination) => {
    if (!destination) return;
    setProgressError(null);
    try {
      const visit = await saveTopicVisit(destination.id);
      if (destination.moduleId !== Number(moduleId)) {
        navigate(`/courses/${courseId}/modules/${destination.moduleId}?topic=${destination.id}`);
        return;
      }
      setSelectedTopicId(destination.id);
      markTopicStatus(destination.id, visit.status);
      navigate(`/courses/${courseId}/modules/${moduleId}?topic=${destination.id}`, { replace: true });
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (visitError) {
      setProgressError(visitError.message);
    }
  };

  useEffect(() => {
    let active = true;
    async function loadModule() {
      try {
        setIsLoading(true);
        setError(null);
        setProgressError(null);
        const data = await getModule();
        if (!active) return;
        const requestedTopicId = Number(new URLSearchParams(window.location.search).get("topic"));
        const initialTopic = data.module.topics?.find((topic) => topic.id === requestedTopicId)
          ?? data.module.topics?.find((topic) => topic.id === data.last_topic_id)
          ?? data.module.topics?.[0]
          ?? null;
        setModule(data.module);
        setOutline(data.course_outline ?? []);
        setCourseProgress(data.course_progress);
        setSelectedTopicId(initialTopic?.id ?? null);
        if (initialTopic) {
          try {
            const visit = await saveTopicVisit(initialTopic.id);
            if (active) markTopicStatus(initialTopic.id, visit.status);
          } catch (visitError) {
            if (active) setProgressError(visitError.message);
          }
        }
      } catch (loadError) {
        if (active) setError(loadError.message);
      } finally {
        if (active) setIsLoading(false);
      }
    }
    loadModule();
    return () => { active = false; };
  }, [getModule, markTopicStatus, saveTopicVisit]);

  const topics = module?.topics ?? [];
  const selectedTopic = topics.find((topic) => topic.id === selectedTopicId) ?? null;
  const selectedLesson = selectedTopic?.lessons?.[0];
  const flatTopics = useMemo(() => outline.flatMap((moduleItem) =>
    moduleItem.topics.map((topic) => ({ ...topic, moduleId: moduleItem.id, moduleTitle: moduleItem.title }))
  ), [outline]);
  const currentIndex = flatTopics.findIndex((topic) => topic.id === selectedTopicId);
  const previousTopic = currentIndex > 0 ? flatTopics[currentIndex - 1] : null;
  const nextTopic = currentIndex >= 0 ? flatTopics[currentIndex + 1] ?? null : null;

  const completeSelectedTopic = async () => {
    if (!selectedTopic || selectedTopic.status === "completed" || isCompleting) return;
    setIsCompleting(true);
    setProgressError(null);
    try {
      const response = await apiRequest("/api/progress/complete/", {
        method: "POST",
        body: JSON.stringify({ topic: selectedTopic.id }),
      });
      if (!response.ok) throw new Error("Не удалось отметить топик пройденным.");
      const data = await response.json();
      setOutline(data.course_outline);
      setCourseProgress(data.course_progress);
      setModule((current) => current ? {
        ...current,
        status: data.course_outline.find((item) => item.id === current.id)?.status,
        topics: current.topics.map((topic) => topic.id === selectedTopic.id ? { ...topic, status: "completed" } : topic),
      } : current);
    } catch (completeError) {
      setProgressError(completeError.message);
    } finally {
      setIsCompleting(false);
    }
  };

  if (isLoading) return <p className="module-page-state" role="status">Загрузка модуля…</p>;
  if (error) return <p className="module-page-state" role="alert">{error}</p>;

  return (
    <div className="module-page"><main>
      <section className="module-page-top"><div className="container">
        <Link to={`/courses/${courseId}`} className="module-page-back">← Назад к курсу</Link>
        <div className="module-page-breadcrumbs"><span>{module?.course_title}</span><span>/</span><span>{module?.title}</span></div>
      </div></section>

      <section className="module-page-header"><div className="container">
        <span className="module-page-label">{selectedTopic?.title ?? "Материалы курса"}</span>
        <h1>{module?.title}</h1><p>{module?.description}</p>
        <div className="module-page-progress">
          <div className="module-page-progress-bar" aria-hidden="true"><div className="module-page-progress-fill" style={{ width: `${courseProgress?.percent ?? 0}%` }} /></div>
          <span>{courseProgress?.completed_topics ?? 0} из {courseProgress?.total_topics ?? 0} пройдено</span>
        </div>
      </div></section>

      <section className="module-page-content"><div className="container module-page-grid">
        <aside className="module-page-topics-sidebar" aria-label="Содержание курса">
          <div className="course-outline-heading"><div><span>Содержание</span><h2>Модули курса</h2></div><strong>{courseProgress?.percent ?? 0}%</strong></div>
          {outline.length === 0 ? <p>В курсе пока нет модулей.</p> : (
            <ol className="course-outline">
              {outline.map((moduleItem, moduleIndex) => (
                <li key={moduleItem.id} className={`course-outline-module is-${moduleItem.status} ${moduleItem.id === Number(moduleId) ? "is-current" : ""}`}>
                  <Link className="course-outline-module-link" to={`/courses/${courseId}/modules/${moduleItem.id}${moduleItem.topics[0] ? `?topic=${moduleItem.topics[0].id}` : ""}`}>
                    <span className="course-outline-module-number">{moduleIndex + 1}</span>
                    <span className="course-outline-module-copy"><strong>{moduleItem.title}</strong><small>{STATUS_LABELS[moduleItem.status]}</small></span>
                    <span className="course-outline-status" aria-label={STATUS_LABELS[moduleItem.status]}>{moduleItem.status === "completed" ? "✓" : ""}</span>
                  </Link>
                  <ol className="module-page-topics">
                    {moduleItem.topics.map((topic, topicIndex) => (
                      <li key={topic.id} className={`is-${topic.status} ${topic.id === selectedTopicId ? "is-active" : ""}`}>
                        {moduleItem.id === Number(moduleId) ? (
                          <button type="button" onClick={() => openTopic({ ...topic, moduleId: moduleItem.id })} aria-current={topic.id === selectedTopicId ? "step" : undefined}>
                            <span className="module-page-topic-number">{topic.status === "completed" ? "✓" : topicIndex + 1}</span>
                            <span className="module-page-topic-copy"><strong>{topic.title}</strong><small>{STATUS_LABELS[topic.status]}</small></span>
                          </button>
                        ) : (
                          <Link to={`/courses/${courseId}/modules/${moduleItem.id}?topic=${topic.id}`}>
                            <span className="module-page-topic-number">{topic.status === "completed" ? "✓" : topicIndex + 1}</span>
                            <span className="module-page-topic-copy"><strong>{topic.title}</strong><small>{STATUS_LABELS[topic.status]}</small></span>
                          </Link>
                        )}
                      </li>
                    ))}
                  </ol>
                </li>
              ))}
            </ol>
          )}
        </aside>

        <article className="module-page-lesson">
          {progressError && <p className="module-progress-error" role="alert">{progressError}</p>}
          {selectedTopic ? <>
            <div className="lesson-status-row"><span className="module-page-lesson-type">{selectedTopic.title}</span><span className={`lesson-status is-${selectedTopic.status}`}>{STATUS_LABELS[selectedTopic.status]}</span></div>
            {selectedLesson ? <MarkdownContent content={selectedLesson.content} /> : <p>В этом топике пока нет материала.</p>}
            <div className="topic-completion"><div><strong>{selectedTopic.status === "completed" ? "Топик пройден" : "Материал изучен?"}</strong><p>{selectedTopic.status === "completed" ? "Результат сохранён в вашем прогрессе." : "Отметьте топик пройденным, когда закончите изучение."}</p></div>
              <button type="button" onClick={completeSelectedTopic} disabled={selectedTopic.status === "completed" || isCompleting}>{selectedTopic.status === "completed" ? "✓ Пройдено" : isCompleting ? "Сохраняем…" : "Завершить топик"}</button>
            </div>
          </> : <p>В этом модуле пока нет топиков.</p>}

          {selectedTopic && <nav className="lesson-navigation" aria-label="Навигация между топиками">
            <button type="button" className="lesson-navigation-button lesson-navigation-button--previous" onClick={() => openTopic(previousTopic)} disabled={!previousTopic}><span className="lesson-navigation-arrow" aria-hidden="true">←</span><span className="lesson-navigation-copy"><small>Предыдущий топик</small><strong>{previousTopic?.title ?? "Начало курса"}</strong></span></button>
            <button type="button" className="lesson-navigation-button lesson-navigation-button--next" onClick={() => openTopic(nextTopic)} disabled={!nextTopic}><span className="lesson-navigation-copy"><small>Следующий топик</small><strong>{nextTopic?.title ?? "Курс завершён"}</strong></span><span className="lesson-navigation-arrow" aria-hidden="true">→</span></button>
          </nav>}
          {courseProgress?.status === "completed" && <div className="course-complete-message" role="status"><strong>Курс пройден!</strong><span>Все топики отмечены как завершённые.</span></div>}
        </article>
      </div></section>
    </main></div>
  );
}

export default ModulePage;
