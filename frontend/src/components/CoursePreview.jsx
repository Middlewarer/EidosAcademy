import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "./api/apiRequest";
import FavoriteButton from "./FavoriteButton";
import CourseSkeleton from "./CourseSkeleton";
export default function CoursePreview({ course, onClose }) {
  const dialog = useRef(null);
  const [detail, setDetail] = useState(null);
  const [error, setError] = useState(false);
  useEffect(() => {
    const element = dialog.current;
    const previous = document.activeElement;
    element.showModal();
    return () => { element.close(); previous?.focus(); };
  }, []);
  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const response = await apiRequest(`/api/courses/${course.id}/`, { auth: false });
        if (!response.ok) throw new Error();
        const data = await response.json();
        if (active) setDetail(data);
      } catch { if (active) setError(true); }
    }
    load();
    return () => { active = false; };
  }, [course.id]);
  return <dialog ref={dialog} className="course-preview" aria-labelledby="preview-title"
    onCancel={onClose} onClick={(event) => { if (event.target === dialog.current) onClose(); }}>
    <div className="course-preview__body">
      <button type="button" className="learning-button" onClick={onClose} autoFocus>Закрыть ✕</button>
      <h2 id="preview-title">{course.title}</h2>
      <p>{detail?.course.short_description || course.description}</p>
      {!detail && !error && <CourseSkeleton />}
      {error && <p role="alert">Программа не загрузилась. Попробуйте открыть страницу курса.</p>}
      {detail && <><p>{detail.module_counter} модулей · {detail.topic_counter} тем</p><h3>Программа</h3>
        {detail.course.modules.length ? <ol>{detail.course.modules.map((module) =>
          <li key={module.id}>{module.title}</li>)}</ol> : <p>Программа готовится.</p>}</>}
      <div className="learning-actions">
        <Link className="learning-button learning-button--primary" to={`/courses/${course.id}`} onClick={onClose}>Открыть курс →</Link>
        <FavoriteButton id={course.id} />
      </div>
    </div>
  </dialog>;
}
