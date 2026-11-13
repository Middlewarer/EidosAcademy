import { useState } from "react"
import CourseCard from "../CourseCard"
import CourseSkeleton from "../CourseSkeleton";
import { useFavorites } from "../context/FavoritesContext";
import { Link } from "react-router-dom";

const CoursesList = (props) => {
  const {activeFilter, search, favoritesOnly, courses, loading, error, onRetry} = props
  const { ids } = useFavorites();
  const [pagination, setPagination] = useState({ key: "", page: 1 });
  const [pageSize, setPageSize] = useState(6);

    const filteredCourses = courses.filter((course) => {
    if (activeFilter === "All") {
        return true;
    }
    return course.title.toLocaleLowerCase().includes(activeFilter.toLocaleLowerCase());
}).filter((course) => {
  const query = search.trim().toLocaleLowerCase("ru-RU");
  const searchable = [course.title, course.category, course.short_description, course.description]
    .filter(Boolean).join(" ").toLocaleLowerCase("ru-RU");
  return searchable.includes(query);
})
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
        <section className="pb-24" id="catalog-results">
          <div className="mx-auto w-[min(1200px,calc(100%_-_48px))] max-sm:w-[calc(100%_-_28px)]">
            {!loading && !error && <div className="mb-6 flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-[var(--line)] bg-[var(--white)] px-5 py-4">
              <p className="m-0 text-sm font-semibold text-[var(--muted)]" aria-live="polite">Найдено курсов: {filteredCourses.length}</p>
              <label className="flex items-center gap-2 text-sm font-semibold text-[var(--muted)]">На странице <select className="rounded-lg border border-[var(--line)] bg-[var(--paper)] px-3 py-2 text-[var(--ink)] outline-none focus:border-[var(--blue)]" value={pageSize} onChange={(event) => setPageSize(Number(event.target.value))}>
                <option value={3}>3</option><option value={6}>6</option><option value={12}>12</option>
              </select></label>
            </div>}

            {loading && <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">{[1, 2, 3].map((id) => <CourseSkeleton key={id} />)}</div>}
            {error && (
              <div className="rounded-2xl border border-red-300 bg-red-50 p-6 text-red-900 dark:border-red-900 dark:bg-red-950/30 dark:text-red-200" role="alert">
                <p className="m-0">{error}</p>
                <button type="button" className="mt-4 rounded-xl bg-red-700 px-4 py-2.5 font-bold text-white transition hover:bg-red-800" onClick={onRetry}>
                  Попробовать снова
                </button>
              </div>
            )}
            {!loading && !error && filteredCourses.length === 0 && (
              <div className="rounded-3xl border border-dashed border-[var(--line)] bg-[var(--white)] px-6 py-16 text-center"><h2 className="text-2xl font-extrabold">{favoritesOnly ? "Здесь пока нет подходящих курсов" : "Курсы не найдены"}</h2>
                <p className="mx-auto mt-3 max-w-xl text-[var(--muted)]">{favoritesOnly ? "Нажмите «Отложить курс» в каталоге или измените фильтры." : "Попробуйте изменить запрос или выбрать все курсы."}</p>
                {favoritesOnly && <Link className="mt-6 inline-flex rounded-xl bg-[var(--blue)] px-5 py-3 font-bold text-white no-underline" to="/courses">Открыть каталог →</Link>}
              </div>
            )}

            {!loading && !error && <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
              {visibleCourses.map((course) =>
              (<CourseCard
              key={course.id}
              id={course.id}
              title={course.title}
              image={course.image}
              description={(course.short_description || course.description || "").slice(0, 160)} />))}
            </div>}
            {!loading && !error && filteredCourses.length > 0 && <nav className="mt-10 flex items-center justify-center gap-4" aria-label="Страницы курсов">
              <button className="rounded-xl border border-[var(--line)] bg-[var(--white)] px-4 py-2.5 font-bold text-[var(--ink)] transition hover:border-[var(--blue)] disabled:cursor-not-allowed disabled:opacity-40" disabled={page === 1} onClick={() => changePage(page - 1)}>← Назад</button>
              <span className="min-w-20 text-center text-sm font-bold text-[var(--muted)]" aria-live="polite">{page} / {totalPages}</span>
              <button className="rounded-xl border border-[var(--line)] bg-[var(--white)] px-4 py-2.5 font-bold text-[var(--ink)] transition hover:border-[var(--blue)] disabled:cursor-not-allowed disabled:opacity-40" disabled={page === totalPages} onClick={() => changePage(page + 1)}>Далее →</button>
            </nav>}
          </div>
        </section>
    )
}

export default CoursesList
