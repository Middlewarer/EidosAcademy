import { Link } from "react-router-dom"
import { useState } from "react";
import FavoriteButton from "./FavoriteButton";
import CoursePreview from "./CoursePreview";

const CourseCard = ({ title, description, image, id }) => {
    const [preview, setPreview] = useState(false);
    return (
        <article className="course-card learning-card">
        <Link
          to={`/courses/${id}`}
          className="learning-card__link"
          aria-label={`Подробнее о курсе «${title}»`}
        >

            <div className={`course-cover ${image ? "has-image" : ""}`}>
              {image ? <img src={image} alt={`Обложка курса «${title}»`} loading="lazy" /> : <span aria-hidden="true">{title?.charAt(0)}</span>}
            </div>

            <h3>{title}</h3>

            <p>{description}</p>

            <span className="course-card-cta">
              Подробнее
              <span aria-hidden="true">→</span>
            </span>
        </Link>
        <div className="learning-card__actions">
          <FavoriteButton id={id} />
          <button className="learning-button" type="button" onClick={() => setPreview(true)}>Быстрый просмотр</button>
        </div>
        {preview && <CoursePreview course={{ id, title, description }} onClose={() => setPreview(false)} />}
        </article>
    )
}

export default CourseCard
