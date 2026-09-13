import CourseCard from "../CourseCard"
import { useEffect, useState } from "react"

import { getCourses } from "../api/courses/Courses"


const Courses = () => {
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)



  useEffect(() => {
      async function load() {
        try {
          setError(null)
          const data = await getCourses();
          setCourses(data.courses)
        }
        catch (err) {
          setError(err.message)
        } finally {
          setLoading(false)
        }
      } 
      load();
  }, []);

       return (
        <section id="courses" className="courses">

          <div className="container">


            <div className="section-title">

              <span>
                Направления
              </span>


              <h2>
                Выбери свою технологию
              </h2>


            </div>



            <div className="course-grid">
            {loading && <p role="status">Загрузка курсов…</p>}
            {error && <p role="alert">{error}</p>}
            {!loading && !error && courses.length === 0 && <p>Курсы скоро появятся.</p>}
            
            {courses.map((course) =>
              (<CourseCard
              key={course.id}
              id={course.id}
              title={course.title}
              image={course.image}
              description={ course.description.length > 120 ? course.description.slice(0, 120) + "..." : course.description} />))}
            </div>


          </div>


        </section>

    )
}

export default Courses
