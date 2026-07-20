const CourseCard = (props) => {
    const {
        title,
        description,
        key,
    } = props
    return (
        <article className="course-card">

                <div className="course-icon">
                </div>


                <h3>
                  {title}
                </h3>


                <p>
                  {description}
                </p>


                <button key={key}>
                  Подробнее →
                </button>

              </article>
    )
}

export default CourseCard