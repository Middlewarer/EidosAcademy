import "../styles/ModulePage.css";
import CourseOutline from "../components/CourseOutline";
import MarkdownContent from "../components/MarkdownContent";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
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
  const [searchParams] = useSearchParams();
  const requestedTopic = searchParams.get("topic");
  const [lastTopicId, setLastTopicId] = useState(null);
  const selectionRef = useRef(null);
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

  const openTopic = (destination) => {
    if (!destination) return;
    navigate(`/courses/${courseId}/modules/${destination.moduleId}?topic=${destination.id}`);
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
        if (Number(data.module.course_id) !== Number(courseId)) {
          throw new Error("Этот модуль не относится к выбранному курсу.");
        }
        setModule(data.module);
        setOutline(data.course_outline ?? []);
        setCourseProgress(data.course_progress);
        setLastTopicId(data.last_topic_id);

      } catch (loadError) {
        if (active) setError(loadError.message);
      } finally {
        if (active) setIsLoading(false);
      }
    }
    loadModule();
    return () => { active = false; };
  }, [getModule, courseId]);

  const topics = module?.id === Number(moduleId) ? module.topics ?? [] : [];
  const selectedTopic = requestedTopic
    ? topics.find((topic) => topic.id === Number(requestedTopic)) ?? null
    : topics.find((topic) => topic.id === lastTopicId) ?? topics[0] ?? null;
  const selectedTopicId = selectedTopic?.id;
  selectionRef.current = `${moduleId}:${selectedTopicId}`;
  const lessons = selectedTopic?.lessons ?? [];
  const hasMaterial = lessons.some((lesson) => lesson.content?.trim() || lesson.video_url);
  useEffect(() => {
    if (isLoading || !selectedTopicId) return;
    let active = true;
    setProgressError(null);
    setIsCompleting(false);
    if (!requestedTopic) {
      navigate(`/courses/${courseId}/modules/${moduleId}?topic=${selectedTopicId}`, { replace: true });
      return;
    }
    window.scrollTo({ top: 0, behavior: "instant" });
    saveTopicVisit(selectedTopicId).then((visit) => {
      if (active) markTopicStatus(selectedTopicId, visit.status);
    }).catch((error) => { if (active) setProgressError(error.message); });
    return () => { active = false; };
  }, [selectedTopicId, isLoading, requestedTopic, courseId, moduleId, navigate, saveTopicVisit, markTopicStatus]);
  const flatTopics = useMemo(() => outline.flatMap((moduleItem) =>
    moduleItem.topics.map((topic) => ({ ...topic, moduleId: moduleItem.id, moduleTitle: moduleItem.title }))
  ), [outline]);
  const currentIndex = flatTopics.findIndex((topic) => topic.id === selectedTopicId);
  const previousTopic = currentIndex > 0 ? flatTopics[currentIndex - 1] : null;
  const nextTopic = currentIndex >= 0 ? flatTopics[currentIndex + 1] ?? null : null;

  const completeSelectedTopic = async () => {
    if (!hasMaterial || !selectedTopic || selectedTopic.status === "completed" || isCompleting) return;
    const selection = selectionRef.current;
    setIsCompleting(true);
    setProgressError(null);
    try {
      const response = await apiRequest("/api/progress/complete/", {
        method: "POST",
        body: JSON.stringify({ topic: selectedTopic.id }),
      });
      if (!response.ok) throw new Error("Не удалось отметить тему пройденной.");
      const data = await response.json();
      if (selection !== selectionRef.current) return;
      setOutline(data.course_outline);
      setCourseProgress(data.course_progress);
      setModule((current) => current ? {
        ...current,
        status: data.course_outline.find((item) => item.id === current.id)?.status,
        topics: current.topics.map((topic) => topic.id === selectedTopic.id ? { ...topic, status: "completed" } : topic),
      } : current);
    } catch (completeError) {
      if (selection === selectionRef.current) setProgressError(completeError.message);
    } finally {
      if (selection === selectionRef.current) setIsCompleting(false);
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
        <CourseOutline outline={outline} courseId={courseId} moduleId={Number(moduleId)}
          topicId={selectedTopicId} progress={courseProgress} />

        <article className="module-page-lesson">
          {progressError && <p className="module-progress-error" role="alert">{progressError}</p>}
          {selectedTopic ? <>
            <div className="lesson-status-row"><span className="module-page-lesson-type">{selectedTopic.title}</span><span className={`lesson-status is-${selectedTopic.status}`}>{STATUS_LABELS[selectedTopic.status]}</span></div>
            {hasMaterial ? lessons.map((lesson, index) => (
              <section className="learning-material" key={lesson.id ?? index}>
                {lesson.type === "equal" && <h2>Практическое задание</h2>}
                {lesson.type === "video" && lesson.video_url && /^https?:\/\//i.test(lesson.video_url) && (
                  <a className="learning-video" href={lesson.video_url} target="_blank" rel="noopener noreferrer">Открыть видео ↗ <small>В новой вкладке</small></a>
                )}
                {lesson.content && <MarkdownContent content={lesson.content} />}
              </section>
            )) : <p>Материалы этой темы ещё готовятся. Пока можно перейти к другой теме.</p>}
            <div className="topic-completion"><div><strong>{selectedTopic.status === "completed" ? "Тема пройдена" : "Материал изучен?"}</strong><p>{selectedTopic.status === "completed" ? "Результат сохранён в вашем прогрессе." : "Отметьте тему пройденной, когда закончите изучение."}</p></div>
              <button type="button" onClick={completeSelectedTopic} disabled={!hasMaterial || selectedTopic.status === "completed" || isCompleting}>{selectedTopic.status === "completed" ? "✓ Пройдено" : isCompleting ? "Сохраняем…" : "Завершить тему"}</button>
            </div>
          </> : <p>Выберите доступную тему в содержании курса.</p>}

          {selectedTopic && <nav className="lesson-navigation" aria-label="Навигация между темами">
            <button type="button" className="lesson-navigation-button lesson-navigation-button--previous" onClick={() => openTopic(previousTopic)} disabled={!previousTopic}><span className="lesson-navigation-arrow" aria-hidden="true">←</span><span className="lesson-navigation-copy"><small>Предыдущая тема</small><strong>{previousTopic?.title ?? "Начало курса"}</strong></span></button>
            <button type="button" className="lesson-navigation-button lesson-navigation-button--next" onClick={() => openTopic(nextTopic)} disabled={!nextTopic}><span className="lesson-navigation-copy"><small>Следующая тема</small><strong>{nextTopic?.title ?? "Последняя тема курса"}</strong></span><span className="lesson-navigation-arrow" aria-hidden="true">→</span></button>
          </nav>}
          {courseProgress?.status === "completed" && <div className="course-complete-message" role="status"><strong>Курс пройден!</strong><span>Все темы отмечены как завершённые.</span></div>}
        </article>
      </div></section>
    </main></div>
  );
}

export default ModulePage;
