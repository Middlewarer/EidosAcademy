const CoursesFilter = (props) => {
    const filters = ["All", "Python", "Django"]
    const {activeFilter,
        setActiveFilter,
    } = props
    return (
        <section className="py-7">
          <div className="mx-auto flex w-[min(1200px,calc(100%_-_48px))] flex-wrap gap-3 max-sm:w-[calc(100%_-_28px)]" aria-label="Фильтр курсов">
            {
                filters.map((filter) => (
                  <button key={filter} type="button" aria-pressed={activeFilter === filter}
                    className={`rounded-full border px-5 py-2.5 text-sm font-bold transition hover:-translate-y-0.5 ${activeFilter === filter
                      ? "border-[var(--blue)] bg-[var(--blue)] text-white shadow-lg shadow-blue-500/20"
                      : "border-[var(--line)] bg-[var(--white)] text-[var(--muted)] hover:border-[var(--blue)] hover:text-[var(--blue)]"}`}
                    onClick={() => setActiveFilter(filter)}>
                    {filter === "All" ? "Все курсы" : filter}
                  </button>
                ))
            }
          </div>
        </section>
    )
}

export default CoursesFilter;
