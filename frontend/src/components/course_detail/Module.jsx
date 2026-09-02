import { Link } from "react-router-dom";

const Module = ({ id, courseId, title, topics }) => {
    return (
        <Link
            to={`/courses/${courseId}/modules/${id}`}
            className="course-detail-module-link"
            aria-label={`Открыть модуль «${title}»`}
        >
          <article className="course-detail-module">
            <div className="course-detail-module-heading">
              <h3>{title}</h3>
              <span className="course-detail-module-cta" aria-hidden="true">Открыть →</span>
            </div>

            <ul>
                {topics.map((topic) => (
                    <li key={topic.id}>{topic.title}</li>
                ))}
            </ul>
          </article>
        </Link>
    );
};

export default Module
