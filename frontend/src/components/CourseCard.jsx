import { Link } from "react-router-dom"

const CourseCard = ({ title, description, id }) => {
    return (
        <Link
          to={`/courses/${id}`}
          className="course-card-link"
          aria-label={`Подробнее о курсе «${title}»`}
        >
          <article className="course-card">

            <div className="course-icon"></div>

            <h3>{title}</h3>

            <p>{description}</p>

            <span className="course-card-cta">
              Подробнее
              <span aria-hidden="true">→</span>
            </span>
          </article>
        </Link>
    )
}

export default CourseCard
