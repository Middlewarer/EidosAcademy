import CourseCard from "../CourseCard"
import { useEffect, useState } from "react"

const Courses = () => {
  const [courses, setCourses] = useState([])


  const getCourses = async () => {
      const response = await fetch("http://127.0.0.1:8000/api/courses/");

      const data = await response.json()  

      setCourses(data.courses);

  }

  useEffect(() => {
      getCourses()
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
              (< CourseCard key={course.id}
              title={course.title}
              description={ course.description.length > 120 ? course.description.slice(0, 120) + "..." : course.description}/>))}
            </div>


          </div>


        </section>

    )
}

export default Courses