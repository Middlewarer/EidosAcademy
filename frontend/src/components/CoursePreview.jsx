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
  return <dialog ref={dialog} className="m-auto w-[min(680px,calc(100%_-_28px))] rounded-3xl border border-[var(--line)] bg-[var(--white)] p-0 text-[var(--ink)] shadow-2xl backdrop:bg-slate-950/60"
    aria-labelledby="preview-title"
    onCancel={onClose} onClick={(event) => { if (event.target === dialog.current) onClose(); }}>
    <div className="p-6 sm:p-8">
      <div className="flex items-start justify-between gap-5">
        <div><span className="text-xs font-extrabold uppercase tracking-wider text-[var(--blue)]">Быстрый просмотр</span>
          <h2 className="mt-2 text-2xl font-extrabold tracking-tight sm:text-3xl" id="preview-title">{course.title}</h2></div>
        <button type="button" className="flex-none rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3 py-2 text-sm font-bold text-[var(--ink)] hover:border-[var(--blue)]" onClick={onClose} autoFocus>Закрыть ✕</button>
      </div>
      <p className="mt-4 leading-7 text-[var(--muted)]">{detail?.course.short_description || course.description}</p>
      {!detail && !error && <CourseSkeleton />}
      {error && <p className="mt-5 rounded-xl bg-red-50 p-4 text-red-700 dark:bg-red-950/30 dark:text-red-300" role="alert">Программа не загрузилась. Попробуйте открыть страницу курса.</p>}
      {detail && <><p className="mt-5 inline-flex rounded-full bg-[var(--blue-soft)] px-3 py-1.5 text-sm font-bold text-[var(--blue)]">{detail.module_counter} модулей · {detail.topic_counter} тем</p><h3 className="mt-6 text-lg font-extrabold">Программа</h3>
        {detail.course.modules.length ? <ol className="mt-3 space-y-2 pl-5 text-[var(--muted)]">{detail.course.modules.map((module) =>
          <li className="pl-1" key={module.id}>{module.title}</li>)}</ol> : <p className="text-[var(--muted)]">Программа готовится.</p>}</>}
      <div className="mt-7 flex flex-wrap gap-3 border-t border-[var(--line)] pt-5">
        <Link className="rounded-xl bg-[var(--blue)] px-5 py-3 font-bold text-white no-underline transition hover:bg-[var(--blue-dark)]" to={`/courses/${course.id}`} onClick={onClose}>Открыть курс →</Link>
        <FavoriteButton id={course.id} />
      </div>
    </div>
  </dialog>;
}
