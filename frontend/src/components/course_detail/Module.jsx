import { Link } from "react-router-dom";

const Module = ({ id, courseId, title, topics }) => {
    return (
        <article className="course-detail-module">
            <h3>
                <Link to={`/courses/${courseId}/modules/${id}`}>{title}</Link>
            </h3>

            <ul>
                {topics.map((topic) => (
                    <li key={topic.id}>{topic.title}</li>
                ))}
            </ul>
        </article>
    );
};

export default Module