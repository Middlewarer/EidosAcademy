import Search from "../Search"

const CoursesHero = (props) => {
  const {search, setSearch, suggestions} = props
    return (
        <section className="relative overflow-visible border-b border-[var(--line)] bg-[radial-gradient(circle_at_82%_18%,rgba(79,109,245,.18),transparent_28%),var(--white)] py-16 sm:py-20">
          <div className="mx-auto w-[min(1200px,calc(100%_-_48px))] max-sm:w-[calc(100%_-_28px)]">
            <span className="text-xs font-extrabold uppercase tracking-[0.18em] text-[var(--blue)]">Каталог</span>

            <h1 className="mt-4 max-w-4xl text-4xl font-extrabold leading-[1.08] tracking-[-0.04em] text-[var(--ink)] sm:text-5xl lg:text-6xl">Найдите курс, который приблизит вас к первой работе</h1>

            <p className="mt-5 max-w-2xl text-base leading-7 text-[var(--muted)] sm:text-lg">
              Изучайте современные технологии разработки через практику,
              реальные проекты и понятные объяснения.
            </p>

            <Search className="mt-8 max-w-2xl" search={search} setSearch={setSearch} suggestions={suggestions} />
          </div>
        </section>
    )
}

export default CoursesHero
