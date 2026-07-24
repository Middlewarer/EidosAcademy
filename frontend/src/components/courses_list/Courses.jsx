import CourseCard from "../CourseCard"
import { useEffect, useState } from "react"

import { getCourses } from "../api/courses/Courses"


const Courses = () => {
  const [courses, setCourses] = useState([])



  useEffect(() => {
      async function load() {
        try {
          const data = await getCourses();
          setCourses(data.courses)
        }
        catch (err) {
          console.log(err)
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
            
            {courses.map((course) =>
              (<CourseCard
              key={course.id}
              id={course.id}
              title={course.title}
              description={ course.description.length > 120 ? course.description.slice(0, 120) + "..." : course.description} />))}
            </div>


          </div>


        </section>

    )
}

export default Courses