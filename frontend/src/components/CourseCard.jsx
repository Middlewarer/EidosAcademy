import { Link } from "react-router-dom"

const CourseCard = ({ title, description, id }) => {
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

              <Link to={`/courses/${id}`}>
                <button type="button">
                  Подробнее →
                </button>
              </Link> 
              </article>
    )
}

export default CourseCard