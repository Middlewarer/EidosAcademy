import { useEffect, useState } from "react"
import CourseCard from "../CourseCard"

import { getCourses } from "../api/courses/Courses.jsx"

const CoursesList = (props) => {
  const {activeFilter, search} = props

    const [courses, setCourses] = useState([])
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [reloadKey, setReloadKey] = useState(0);

    useEffect(() => {
      async function load() {
        try {
          setLoading(true);
          setError(null);
          const data = await getCourses();
          setCourses(data.courses)
        } catch (err) {
          setError(err.message)
        } finally {
          setLoading(false);
        }
      }

      load();
    }, [reloadKey]);

    const filteredCourses = courses.filter((course) => {
    if (activeFilter === "All") {
        return true;
    }
    return course.title.includes(activeFilter);
}).filter((course) => course.title.includes(search));

    

    return (
        <section className="courses-list">
          <div className="container">
            <p className="courses-count">Найдено курсов: {filteredCourses.length}</p>

            {loading && <p role="status">Загрузка курсов…</p>}
            {error && (
              <div role="alert">
                <p>{error}</p>
                <button type="button" onClick={() => setReloadKey((value) => value + 1)}>
                  Попробовать снова
                </button>
              </div>
            )}
            {!loading && !error && filteredCourses.length === 0 && (
              <p>По вашему запросу курсы не найдены.</p>
            )}

            {!loading && !error && <div className="courses-grid">
              {filteredCourses.map((course) =>
              (<CourseCard
              key={course.id}
              id={course.id}
              title={course.title}
              description={ course.description.length > 120 ? course.description.slice(0, 120) + "..." : course.description} />))}
            </div>}
          </div>
        </section>
    )
}

export default CoursesList
