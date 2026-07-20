import Search from "../Search"

const CoursesHero = (props) => {
  const {search, setSearch} = props
    return (
        <section className="courses-hero">
          <div className="container">
            <span className="courses-label">Каталог</span>

            <h1>Найдите курс, который приблизит вас к первой работе</h1>

            <p>
              Изучайте современные технологии разработки через практику,
              реальные проекты и понятные объяснения.
            </p>

            <Search search={search} setSearch={setSearch} />
          </div>
        </section>
    )
}

export default CoursesHero