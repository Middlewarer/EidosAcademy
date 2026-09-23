import { useEffect, useState } from "react"
import CourseCard from "../CourseCard"
import CourseSkeleton from "../CourseSkeleton";
import { useFavorites } from "../context/FavoritesContext";
import { Link } from "react-router-dom";

import { getCourses } from "../api/courses/Courses.jsx"

const CoursesList = (props) => {
  const {activeFilter, search, favoritesOnly} = props
  const { ids } = useFavorites();
  const [pagination, setPagination] = useState({ key: "", page: 1 });
  const [pageSize, setPageSize] = useState(6);

    const [courses, setCourses] = useState([])
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
          if (active) setCourses(data.courses)
        } catch (err) {
          if (active) setError(err.message)
        } finally {
          if (active) setLoading(false);
        }
      }

      load();
      return () => { active = false; };
    }, [reloadKey]);

    const filteredCourses = courses.filter((course) => {
    if (activeFilter === "All") {
        return true;
    }
    return course.title.toLocaleLowerCase().includes(activeFilter.toLocaleLowerCase());
}).filter((course) => course.title.toLocaleLowerCase().includes(search.trim().toLocaleLowerCase()))
  .filter((course) => !favoritesOnly || ids.includes(course.id));
    const paginationKey = `${activeFilter}:${search}:${favoritesOnly}:${pageSize}`;
    const totalPages = Math.max(1, Math.ceil(filteredCourses.length / pageSize));
    const page = Math.min(pagination.key === paginationKey ? pagination.page : 1, totalPages);
    const visibleCourses = filteredCourses.slice((page - 1) * pageSize, page * pageSize);
    function changePage(next) {
      setPagination({ key: paginationKey, page: next });
      document.getElementById("catalog-results")?.scrollIntoView({ block: "start" });
    }

    

    return (
        <section className="courses-list" id="catalog-results">
          <div className="container">
            {!loading && !error && <div className="learning-toolbar d-flex flex-wrap justify-content-between align-items-center">
              <p className="courses-count" aria-live="polite">Найдено курсов: {filteredCourses.length}</p>
              <label>На странице <select value={pageSize} onChange={(event) => setPageSize(Number(event.target.value))}>
                <option value={3}>3</option><option value={6}>6</option><option value={12}>12</option>
              </select></label>
            </div>}

            {loading && <div className="courses-grid">{[1, 2, 3].map((id) => <CourseSkeleton key={id} />)}</div>}
            {error && (
              <div role="alert">
                <p>{error}</p>
                <button type="button" onClick={() => setReloadKey((value) => value + 1)}>
                  Попробовать снова
                </button>
              </div>
            )}
            {!loading && !error && filteredCourses.length === 0 && (
              <div className="learning-empty"><h2>{favoritesOnly ? "Здесь пока нет подходящих курсов" : "Курсы не найдены"}</h2>
                <p>{favoritesOnly ? "Нажмите «Отложить курс» в каталоге или измените фильтры." : "Попробуйте изменить запрос или выбрать все курсы."}</p>
                {favoritesOnly && <Link to="/courses">Открыть каталог →</Link>}
              </div>
            )}

            {!loading && !error && <div className="courses-grid">
              {visibleCourses.map((course) =>
              (<CourseCard
              key={course.id}
              id={course.id}
              title={course.title}
              image={course.image}
              description={(course.short_description || course.description || "").slice(0, 160)} />))}
            </div>}
            {!loading && !error && filteredCourses.length > 0 && <nav className="learning-pagination" aria-label="Страницы курсов">
              <button className="learning-button" disabled={page === 1} onClick={() => changePage(page - 1)}>← Назад</button>
              <span aria-live="polite">{page} / {totalPages}</span>
              <button className="learning-button" disabled={page === totalPages} onClick={() => changePage(page + 1)}>Далее →</button>
            </nav>}
          </div>
        </section>
    )
}

export default CoursesList
