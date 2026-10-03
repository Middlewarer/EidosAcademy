import "../styles/Courses.css";
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
    <div className="courses-page">
      <main>
        <Crumbs items={[{ label: favoritesOnly ? "Избранные курсы" : "Курсы" }]} />
        {favoritesOnly ? <section className="container learning-intro"><h1>Избранные курсы</h1>
          <p>Сохраните интересные направления и возвращайтесь, когда будете готовы учиться. Список хранится в этом браузере.</p>
          {ids.length > 0 && <p><button className="learning-button" onClick={clear}>Очистить избранное ({ids.length})</button></p>}
          <Search className="courses-search courses-search--favorites" search={search} setSearch={setSearch}
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
