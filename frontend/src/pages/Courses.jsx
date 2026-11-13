import CoursesHero from "../components/courses_list/CoursesHero";
import CoursesFilter from "../components/courses_list/CoursesFilter";
import CoursesList from "../components/courses_list/CoursesList";
import { useEffect, useState } from "react";
import Crumbs from "../components/Crumbs";
import { useFavorites } from "../components/context/FavoritesContext";
import { getCourses } from "../components/api/courses/Courses.jsx";
import Search from "../components/Search";

function Courses({ favoritesOnly = false }) {
  const { ids, clear } = useFavorites();
  const [activeFilter, setActiveFilter] = useState("All");
  const [search, setSearch] = useState("");
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        setLoading(true);
        setError(null);
        const data = await getCourses();
        if (active) setCourses(data.courses || []);
      } catch (requestError) {
        if (active) setError(requestError.message);
      } finally {
        if (active) setLoading(false);
      }
    }
    load();
    return () => { active = false; };
  }, [reloadKey]);

  const searchSuggestions = [...new Set(courses.flatMap((course) => [course.title, course.category]).filter(Boolean))];
  return (
    <div className="min-h-screen bg-[var(--paper)] pt-[74px] text-[var(--ink)]">
      <main>
        <Crumbs items={[{ label: favoritesOnly ? "Избранные курсы" : "Курсы" }]} />
        {favoritesOnly ? <section className="mx-auto w-[min(1200px,calc(100%_-_48px))] py-12 max-sm:w-[calc(100%_-_28px)]">
          <span className="text-xs font-extrabold uppercase tracking-[0.18em] text-[var(--blue)]">Личная подборка</span>
          <h1 className="mt-3 text-4xl font-extrabold tracking-tight sm:text-5xl">Избранные курсы</h1>
          <p className="mt-4 max-w-2xl leading-7 text-[var(--muted)]">Сохраните интересные направления и возвращайтесь, когда будете готовы учиться. Список хранится в этом браузере.</p>
          {ids.length > 0 && <button className="mt-6 rounded-xl border border-[var(--line)] bg-[var(--white)] px-4 py-2.5 font-bold text-[var(--ink)] transition hover:-translate-y-0.5 hover:border-[var(--blue)]" onClick={clear}>Очистить избранное ({ids.length})</button>}
          <Search className="mt-7 max-w-2xl" search={search} setSearch={setSearch}
            suggestions={searchSuggestions} placeholder="Поиск в избранном..." storageKey="eidos-recent-favorite-searches" />
        </section> : <CoursesHero search={search} setSearch={setSearch} suggestions={searchSuggestions} />}

        <CoursesFilter activeFilter={activeFilter} setActiveFilter={setActiveFilter}/>

        <CoursesList activeFilter={activeFilter} search={search} favoritesOnly={favoritesOnly}
          courses={courses} loading={loading} error={error} onRetry={() => setReloadKey((value) => value + 1)} />
      </main>
    </div>
  );
}

export default Courses;
