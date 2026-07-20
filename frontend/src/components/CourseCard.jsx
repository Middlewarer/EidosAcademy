import { Link } from "react-router-dom"

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

              <Link to={"/details"}>
              
                <button key={key}>
                  Подробнее →
                </button>
              </Link> 
              </article>
    )
}

export default CourseCard