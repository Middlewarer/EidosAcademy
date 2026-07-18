const CourseCard = (props) => {
    const {
        title,
        description
    } = props
    return (
        <article className="course-card">

                <div className="course-icon">
                  PY
                </div>


                <h3>
                  {title}
                </h3>


                <p>
                  {description}
                </p>


                <button>
                  Подробнее →
                </button>

              </article>
    )
}

export default CourseCard