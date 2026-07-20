import { Link } from "react-router-dom";

const Crumbs = () => {
    return (
        <section className="course-detail-top">
          <div className="container">
            <Link to={"/courses"} className="course-detail-back">
              ← Назад к каталогу
            </Link>
          </div>
        </section>
    )
}

export default Crumbs;