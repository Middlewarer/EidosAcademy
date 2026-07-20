import Button from "../Button"

const CoursesFilter = (props) => {
    const filters = ["All", "Python", "Django"]
    const {activeFilter,
        setActiveFilter,
    } = props
    return (
        <section className="courses-filters">
          <div className="container courses-filters-list">
            {
                filters.map((filter) => (<Button key={filter} className={activeFilter === filter ? "is-active" : ""} onClick={() => setActiveFilter(filter)}> {filter} </Button>))
            }
          </div>
        </section>
    )
}

export default CoursesFilter;